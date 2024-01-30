# Function to parse Customer from Green Button XML
def parse_customer(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    customers = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        customer_account_id = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}postalAddress/{http://naesb.org/espi/customer}postalCode').text
        organization_name = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}name').text
        building_name = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}buildingName').text
        suite_number = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}suiteNumber').text
        street_address_general = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}addressGeneral').text
        town_name = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}name').text
        county = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}county').text
        state_or_province = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}stateOrProvince').text
        country = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}streetAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}country').text
        postal_code = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}postalAddress/{http://naesb.org/espi/customer}postalCode').text
        phone1_country_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}countryCode').text)
        phone1_area_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}areaCode').text)
        phone1_city_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}cityCode').text)
        phone1_local_number = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}localNumber').text)
        phone2_country_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}countryCode').text)
        phone2_area_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}areaCode').text)
        phone2_city_code = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}cityCode').text)
        phone2_local_number = int(entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}localNumber').text)
        email1 = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}Organization/{http://naesb.org/espi/customer}electronicAddress/{http://naesb.org/espi/customer}email1').text
        customer_kind = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}kind').text
        locale = entry.find('.//{http://naesb.org/espi}Customer/{http://naesb.org/espi/customer}locale').text
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        customers.append({
            'CustomerAccountID': customer_account_id,
            'OrganizationName': organization_name,
            'BuildingName': building_name,
            'SuiteNumber': suite_number,
            'StreetAddressGeneral': street_address_general,
            'TownName': town_name,
            'County': county,
            'StateOrProvince': state_or_province,
            'Country': country,
            'PostalCode': postal_code,
            'Phone1CountryCode': phone1_country_code,
            'Phone1AreaCode': phone1_area_code,
            'Phone1CityCode': phone1_city_code,
            'Phone1LocalNumber': phone1_local_number,
            'Phone2CountryCode': phone2_country_code,
            'Phone2AreaCode': phone2_area_code,
            'Phone2CityCode': phone2_city_code,
            'Phone2LocalNumber': phone2_local_number,
            'Email1': email1,
            'CustomerKind': customer_kind,
            'Locale': locale,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(customers)

# Load Customer data into Pandas DataFrame
customer_data = parse_customer('green_button_data.xml')

# Write Customer data to SQL Server table
customer_data.to_sql('Customer', con=engine, if_exists='replace', index=False)
