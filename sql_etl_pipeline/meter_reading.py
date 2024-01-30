# Function to parse MeterReading from Green Button XML
def parse_meter_reading(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    meter_readings = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        usage_point_id = entry.find('.//{http://naesb.org/espi}UsagePoint/{http://naesb.org/espi}id').text
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        meter_readings.append({
            'UsagePointID': usage_point_id,
            'Title': title,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(meter_readings)

# Load MeterReading data into Pandas DataFrame
meter_reading_data = parse_meter_reading('green_button_data.xml')

# Write data to SQL Server table
meter_reading_data.to_sql('MeterReading', con=engine, if_exists='replace', index=False)
