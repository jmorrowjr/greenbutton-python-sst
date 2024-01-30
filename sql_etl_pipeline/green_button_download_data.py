import xml.etree.ElementTree as ET
import pandas as pd
from sqlalchemy import create_engine

# Function to parse Green Button XML and extract relevant data
def parse_green_button_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    meter_readings = []
    local_time_params = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        usage_point_id = entry.find('.//{http://naesb.org/espi}UsagePoint/{http://naesb.org/espi}id').text
        reading_type = entry.find('.//{http://naesb.org/espi}ReadingType').text
        reading_value = float(entry.find('.//{http://naesb.org/espi}value').text)
        reading_datetime = entry.find('.//{http://naesb.org/espi}timePeriod/{http://naesb.org/espi}start').text

        meter_readings.append({
            'UsagePointID': usage_point_id,
            'ReadingType': reading_type,
            'ReadingValue': reading_value,
            'ReadingDateTime': reading_datetime
        })

        # Parsing LocalTimeParameters
        time_zone = entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}tzOffset').text
        dst_observation = bool(entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}dstEndRule').text)

        local_time_params.append({
            'UsagePointID': usage_point_id,
            'TimeZone': time_zone,
            'DSTObservance': dst_observation
        })

    return pd.DataFrame(meter_readings), pd.DataFrame(local_time_params)

# Load Green Button ESPI data and LocalTimeParameters into Pandas DataFrames
green_button_data, local_time_params_data = parse_green_button_xml('green_button_data.xml')

# Connect to SQL Server database
engine = create_engine('mssql+pyodbc://username:password@server/database')

# Write Green Button data to SQL Server table
green_button_data.to_sql('MeterReading', con=engine, if_exists='replace', index=False)

# Write LocalTimeParameters data to SQL Server table
local_time_params_data.to_sql('LocalTimeParameters', con=engine, if_exists='replace', index=False)
