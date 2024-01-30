# Function to parse LocalTimeParameters from Green Button XML
def parse_local_time_parameters(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    local_time_params = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        usage_point_id = entry.find('.//{http://naesb.org/espi}UsagePoint/{http://naesb.org/espi}id').text
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
        dst_end_rule = entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}dstEndRule').text
        dst_offset = int(entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}dstOffset').text)
        dst_start_rule = entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}dstStartRule').text
        tz_offset = int(entry.find('.//{http://naesb.org/espi}LocalTimeParameters/{http://naesb.org/espi}tzOffset').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        local_time_params.append({
            'UsagePointID': usage_point_id,
            'Title': title,
            'DSTEndRule': dst_end_rule,
            'DSTOffset': dst_offset,
            'DSTStartRule': dst_start_rule,
            'TZOffset': tz_offset,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(local_time_params)

# Load LocalTimeParameters data into Pandas DataFrame
local_time_params_data = parse_local_time_parameters('green_button_data.xml')

# Write data to SQL Server table
local_time_params_data.to_sql('LocalTimeParameters', con=engine, if_exists='replace', index=False)
