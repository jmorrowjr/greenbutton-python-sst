# Function to parse ReadingType from Green Button XML
def parse_reading_type(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    reading_types = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
        accumulation_behaviour = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}accumulationBehaviour').text)
        commodity = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}commodity').text)
        currency = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}currency').text)
        data_qualifier = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}dataQualifier').text)
        flow_direction = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}flowDirection').text)
        interval_length = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}intervalLength').text)
        kind = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}kind').text)
        phase = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}phase').text)
        power_of_ten_multiplier = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}powerOfTenMultiplier').text)
        time_attribute = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}timeAttribute').text)
        uom = int(entry.find('.//{http://naesb.org/espi}ReadingType/{http://naesb.org/espi}uom').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        reading_types.append({
            'Title': title,
            'AccumulationBehaviour': accumulation_behaviour,
            'Commodity': commodity,
            'Currency': currency,
            'DataQualifier': data_qualifier,
            'FlowDirection': flow_direction,
            'IntervalLength': interval_length,
            'Kind': kind,
            'Phase': phase,
            'PowerOfTenMultiplier': power_of_ten_multiplier,
            'TimeAttribute': time_attribute,
            'UOM': uom,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(reading_types)

# Load ReadingType data into Pandas DataFrame
reading_type_data = parse_reading_type('green_button_data.xml')

# Write data to SQL Server table
reading_type_data.to_sql('ReadingType', con=engine, if_exists='replace', index=False)
