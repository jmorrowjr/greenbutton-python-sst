#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET
import bisect
import functools
import datetime
import pytz

from utils import *
from enums import *

class Resource(object):
    def __init__(self, entry):
        self.link_self    = getLink(entry, 'self')
        self.link_up      = getLink(entry, 'up')
        self.link_related = getLink(entry, 'related', True)
        self.title = getEntity(entry, 'atom:title', lambda e: e.text)

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.title or self.link_self)

    def isParentOf(self, other):
        return other.link_self in self.link_related or other.link_up in self.link_related

class ServicePoint(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(ServicePoint, self).__init__(entry)
        obj = entry.find('./atom:content/espi:UsagePoint', ns)
        self.serviceCategory = getEntity(obj, './espi:ServiceCategory/espi:kind',
                                         lambda e: ServiceCategory(int(e.text)))
        
        self.meterReadings = set()
        for mr in meterReadings:
            if self.isParentOf(mr):
                self.addMeterReading(mr)

    def addMeterReading(self, meterReading):
        assert self.isParentOf(meterReading)
        self.meterReadings.add(meterReading)
        meterReading.usagePoint = self

class ReadingType(Resource):
    def __init__(self, entry):
        super(ReadingType, self).__init__(entry)
        obj = entry.find('./atom:content/espi:ReadingType', ns)
        self.typeGbId = None
        self.accumulationBehaviour = getEntity(obj, 'espi:accumulationBehaviour',
                                               lambda e: AccumulationBehaviourType(int(e.text)))
        self.commodity = getEntity(obj, 'espi:commodity',
                                   lambda e: CommodityType(int(e.text)))
        self.dataQualifier = getEntity(obj, 'espi:dataQualifier',
                                       lambda e: DataQualifierType(int(e.text)))
        self.defaultQuality = getEntity(obj, 'espi:defaultQuality',
                                        lambda e: QualityOfReading(int(e.text)))
        self.flowDirection = getEntity(obj, 'espi:flowDirection',
                                       lambda e: FlowDirectionType(int(e.text)))
        self.intervalLength = getEntity(obj, 'espi:intervalLength', lambda e: int(e.text))
        self.kind = getEntity(obj, 'espi:kind', lambda e: KindType(int(e.text)))
        self.phase = getEntity(obj, 'espi:phase', lambda e: PhaseCode(int(e.text)))
        self.powerOfTenMultiplier = getEntity(obj, 'espi:powerOfTenMultiplier',
                                              lambda e: int(e.text))
        self.timeAttribute = getEntity(obj, 'espi:timeAttribute',
                                       lambda e: TimeAttributeType(int(e.text)))
        self.uom = getEntity(obj, 'espi:uom', lambda e: UomType(int(e.text)))

class MeterReading(Resource):
    def __init__(self, entry, servicePoints=[], readingTypes=[]):
        super(MeterReading, self).__init__(entry)
        self.servicePoints = None
        self.readingType = None
        self.intervalBlocks = []

        for sp in servicePoints:
            if sp.isParentOf(self):
                sp.addMeterReading(self)
        for rt in readingTypes:
            if self.isParentOf(rt):
                self.setReadingType(rt)
                        
    @property
    def intervalReadings(self):
        for ib in self.intervalBlocks:
            for ir in ib.intervalReadings:
                yield ir
    
    def addIntervalBlock(self, intervalBlock):
        assert self.isParentOf(intervalBlock)
        bisect.insort(self.intervalBlocks, intervalBlock)
        intervalBlock.meterReading = self

    def setReadingType(self, readingType):
        assert self.isParentOf(readingType)
        assert self.readingType is None or self.readingType.link_self == readingType.link_self
        self.readingType = readingType

@functools.total_ordering
class IntervalBlock(Resource):
    def __init__(self, entry, meterReadings=[]):
        super(IntervalBlock, self).__init__(entry)
        self.meterReading = None

        obj = entry.find('./atom:content/espi:IntervalBlock', ns)
        self.interval = getEntity(obj, 'espi:interval', lambda e: DateTimeInterval(e))
        self.intervalReadings = sorted([IntervalReading(ir, self) for ir in obj.findall('espi:IntervalReading', ns)])

        for mr in meterReadings:
            if mr.isParentOf(self):
                mr.addIntervalBlock(self)

    def __eq__(self, other):
        if not isinstance(other, IntervalBlock):
            return False
        return self.link_self == other.link_self
    
    def __lt__(self, other):
        return self.interval < other.interval

class IntervalReading:
    def __init__(self, entity, parent):
        self.intervalBlock = parent
        self.value = getEntity(entity, 'espi:value', lambda e: int(e.text))
        self.quality = getEntity(entity, 'espi:ReadingQuality/espi:quality', lambda e: QualityOfReading(int(e.text)))
        self.duration = getEntity(entity, 'espi:timePeriod/espi:duration', lambda e: int(e.text))
        self.local_unix_time = getEntity(entity, 'espi:timePeriod/espi:start', lambda e: int(e.text))

    def __repr__(self):
        return '<IntervalReading (%s, %s: %s %s)>' % (self.local_unix_time, self.duration, self.value)

    def __eq__(self, other):
        if not isinstance(other, IntervalReading):
            return False
        return (self.local_unix_time, self.value) == (other.local_unix_time, other.value)
    
    def __lt__(self, other):
        if not isinstance(other, IntervalReading):
            return False
        return (self.local_unix_time, self.value) < (other.local_unix_time, other.value)    
         
@functools.total_ordering
class DateTimeInterval:
    def __init__(self, entity):
        self.duration = getEntity(entity, 'espi:duration',
                                  lambda e: datetime.timedelta(seconds=int(e.text)))
        # Convert the string timestamp to an integer and create the initial UTC datetime
        self.start = getEntity(entity, 'espi:start',
                               lambda e: datetime.datetime.fromtimestamp(int(e.text), pytz.timezone("UTC")))
        
    def __repr__(self):
        return '<DateTimeInterval (%s, %s)>' % (self.start, self.duration)

    def __eq__(self, other):
        if not isinstance(other, DateTimeInterval):
            return False
        return (self.start, self.duration) == (other.start, other.duration)
    
    def __lt__(self, other):
        if not isinstance(other, DateTimeInterval):
            return False
        return (self.start, self.duration) < (other.start, other.duration)
        

def parse_feed(filename):
    tree = ET.parse(filename)

    readingTypes = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:ReadingType/../..', ns):
        rt = ReadingType(entry)
        readingTypes.append(rt)

    servicePoints = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:UsagePoint/../..', ns):
        sp = ServicePoint(entry)
        servicePoints.append(sp)
    
    meterReadings = []    
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:MeterReading/../..', ns):
        mr = MeterReading(entry, servicePoints=servicePoints, readingTypes=readingTypes)
        meterReadings.append(mr)

    intervalBlocks = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:IntervalBlock/../..', ns):
        ib = IntervalBlock(entry, meterReadings=meterReadings)
        intervalBlocks.append(ib)

    print(readingTypes, servicePoints, meterReadings, intervalBlocks)
    return meterReadings


if __name__ == '__main__':
    meterReadings = parse_feed(sys.argv[1])

    for mr in meterReadings:
        print('  Meter Reading (%s):' % (mr.title))
        for ir in mr.intervalReadings:
            print('    %s, %s, %s' % (ir.local_unix_time, ir.value, ir.quality.name), end = '\n')
            
