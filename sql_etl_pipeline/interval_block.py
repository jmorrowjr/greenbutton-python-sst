# Function to parse IntervalBlock and IntervalReading from Green Button XML
def parse_interval_block(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    interval_blocks = []
    interval_readings = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        meter_reading_id = entry.find('.//{http://naesb.org/espi}IntervalBlock/{http://naesb.org/espi}interval/{http://naesb.org/espi}start').text
        duration = int(entry.find('.//{http://naesb.org/espi}IntervalBlock/{http://naesb.org/espi}interval/{http://naesb.org/espi}duration').text)
        start = int(entry.find('.//{http://naesb.org/espi}IntervalBlock/{http://naesb.org/espi}interval/{http://naesb.org/espi}start').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        interval_blocks.append({
            'MeterReadingID': meter_reading_id,
            'Duration': duration,
            'Start': start,
            'Published': published,
            'Updated': updated
        })

        for interval_reading in entry.findall('.//{http://naesb.org/espi}IntervalBlock/{http://naesb.org/espi}IntervalReading'):
            cost = float(interval_reading.find('.//{http://naesb.org/espi}cost').text)
            time_period_duration = int(interval_reading.find('.//{http://naesb.org/espi}timePeriod/{http://naesb.org/espi}duration').text)
            time_period_start = int(interval_reading.find('.//{http://naesb.org/espi}timePeriod/{http://naesb.org/espi}start').text)
            value = int(interval_reading.find('.//{http://naesb.org/espi}value').text)

            interval_readings.append({
                'IntervalBlockID': meter_reading_id,
                'Cost': cost,
                'TimePeriodDuration': time_period_duration,
                'TimePeriodStart': time_period_start,
                'Value': value
            })

    return pd.DataFrame(interval_blocks), pd.DataFrame(interval_readings)

# Load IntervalBlock and IntervalReading data into Pandas DataFrames
interval_block_data, interval_reading_data = parse_interval_block('green_button_data.xml')

# Write IntervalBlock data to SQL Server table
interval_block_data.to_sql('IntervalBlock', con=engine, if_exists='replace', index=False)

# Write IntervalReading data to SQL Server table
interval_reading_data.to_sql('IntervalReading', con=engine, if_exists='replace', index=False)
