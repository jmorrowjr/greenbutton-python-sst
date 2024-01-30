# Function to parse CustomerAccount from Green Button XML
def parse_customer_account(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    customer_accounts = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        customer_account_id = entry.find('.//{http://www.w3.org/2005/Atom}id').text
        customer_id = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}name').text
        billing_cycle = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}billingCycle').text
        created_datetime = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}createdDateTime').text
        last_modified_datetime = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}lastModifiedDateTime').text
        email1 = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}electronicAddress/{http://naesb.org/espi/customer}email1').text
        main_building_name = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}buildingName').text
        main_suite_number = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}suiteNumber').text
        main_address_general = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}streetDetail/{http://naesb.org/espi/customer}addressGeneral').text
        main_town_name = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}name').text
        main_county = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}county').text
        main_state_or_province = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}stateOrProvince').text
        main_country = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}country').text
        main_postal_code = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}mainAddress/{http://naesb.org/espi/customer}townDetail/{http://naesb.org/espi/customer}postalCode').text
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        customer_accounts.append({
            'CustomerAccountID': customer_account_id,
            'CustomerID': customer_id,
            'BillingCycle': billing_cycle,
            'CreatedDateTime': created_datetime,
            'LastModifiedDateTime': last_modified_datetime,
            'Email1': email1,
            'MainBuildingName': main_building_name,
            'MainSuiteNumber': main_suite_number,
            'MainAddressGeneral': main_address_general,
            'MainTownName': main_town_name,
            'MainCounty': main_county,
            'MainStateOrProvince': main_state_or_province,
            'MainCountry': main_country,
            'MainPostalCode': main_postal_code,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(customer_accounts)

# Load CustomerAccount data into Pandas DataFrame
customer_account_data = parse_customer_account('green_button_data.xml')

# Write CustomerAccount data to SQL Server table
customer_account_data.to_sql('CustomerAccount', con=engine, if_exists='replace', index=False)
