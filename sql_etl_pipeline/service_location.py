# Function to parse ServiceLocation from Green Button XML
def parse_service_location(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    service_locations = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        service_location_id = entry.find('.//{http://www.w3.org/2005/Atom}id').text
        customer_id = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}name').text
        name = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}name').text
        location_type = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}type').text
        main_address_building_name = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}buildingName').text
        main_address_suite_number = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}suiteNumber').text
        main_address_street = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}addressGeneral').text
        main_address_city = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}name').text
        main_address_county = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}county').text
        main_address_state = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}stateOrProvince').text
        main_address_country = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}country').text
        main_address_postal_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}postalCode').text
        secondary_address_building_name = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}buildingName').text
        secondary_address_suite_number = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}suiteNumber').text
        secondary_address_street = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}addressGeneral').text
        secondary_address_city = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}name').text
        secondary_address_county = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}county').text
        secondary_address_state = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}stateOrProvince').text
        secondary_address_country = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}country').text
        secondary_address_postal_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}secondaryAddress/{http://naesb.org/espi/customer}postalCode').text
        phone1_country_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}countryCode').text
        phone1_area_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}areaCode').text
        phone1_city_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}cityCode').text
        phone1_local_number = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone1/{http://naesb.org/espi/customer}localNumber').text
        phone2_country_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}countryCode').text
        phone2_area_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}areaCode').text
        phone2_city_code = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}cityCode').text
        phone2_local_number = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}phone2/{http://naesb.org/espi/customer}localNumber').text
        email1 = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}electronicAddress/{http://naesb.org/espi/customer}email1').text
        direction = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}direction').text
        status_value = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}status/{http://naesb.org/espi/customer}value').text
        status_datetime = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}status/{http://naesb.org/espi/customer}dateTime').text
        status_reason = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}status/{http://naesb.org/espi/customer}reason').text
        access_method = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}accessMethod').text
        needs_inspection = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}needsInspection').text
        outage_block = entry.find('.//{http://naesb.org/espi/customer}ServiceLocation/{http://naesb.org/espi/customer}outageBlock').text
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        service_locations.append({
            'title': value,
            'title': value,
            'SecondaryAddressCity': secondary_address_city,
            'SecondaryAddressCounty': secondary_address_county,
            'SecondaryAddressState': secondary_address_state,
            'SecondaryAddressCountry': secondary_address_country,
            'SecondaryAddressPostalCode': secondary_address_postal_code,
            'Phone1CountryCode': phone1_country_code,
            'Phone1AreaCode': phone1_area_code,
            'Phone1CityCode': phone1_city_code,
            'Phone1LocalNumber': phone1_local_number,
            'Phone2CountryCode': phone2_country_code,
            'Phone2AreaCode': phone2_area_code,
            'Phone2CityCode': phone2_city_code,
            'Phone2LocalNumber': phone2_local_number,
            'Email1': email1,
            'Direction': direction,
            'StatusValue': status_value,
            'StatusDatetime': status_datetime,
            'StatusReason': status_reason,
            'AccessMethod': access_method,
            'NeedsInspection': needs_inspection,
            'OutageBlock': outage_block,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(service_locations)

# Load ReadingType data into Pandas DataFrame
service_location_data = parse_service_location('green_button_data.xml')

# Write data to SQL Server table
service_location_data.to_sql('ServiceLocation', con=engine, if_exists='replace', index=False)
