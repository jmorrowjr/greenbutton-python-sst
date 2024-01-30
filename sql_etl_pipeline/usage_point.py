# Function to parse UsagePoint from Green Button XML
def parse_usage_point(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    usage_points = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        subscription_id = entry.find('.//{http://naesb.org/espi}UsagePoint/{http://naesb.org/espi}ServiceCategory/{http://naesb.org/espi}kind').text
        title = entry.find('.//{http://www.w3.org/2005/Atom}title').text
        service_category_kind = int(entry.find('.//{http://naesb.org/espi}UsagePoint/{http://naesb.org/espi}ServiceCategory/{http://naesb.org/espi}kind').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        usage_points.append({
            'SubscriptionID': subscription_id,
            'Title': title,
            'ServiceCategory': service_category_kind,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(usage_points)

# Load UsagePoint data into Pandas DataFrame
usage_point_data = parse_usage_point('green_button_data.xml')

# Write data to SQL Server table
usage_point_data.to_sql('UsagePoint', con=engine, if_exists='replace', index=False)
