# Function to parse CustomerAgreement from Green Button XML
def parse_customer_agreement(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    customer_agreements = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        customer_agreement_id = entry.find('.//{http://www.w3.org/2005/Atom}id').text
        customer_id = entry.find('.//{http://naesb.org/espi/customer}Customer/{http://naesb.org/espi/customer}name').text
        name = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}name').text
        agreement_type = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}type').text
        created_datetime = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}createdDateTime').text
        last_modified_datetime = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}lastModifiedDateTime').text
        email1 = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}electronicAddress/{http://naesb.org/espi/customer}email1').text
        sign_date = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}signDate').text
        validity_interval_duration = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}validityInterval/{http://naesb.org/espi/customer}duration').text
        validity_interval_start = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}validityInterval/{http://naesb.org/espi/customer}start').text
        is_pre_pay = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}isPrePay').text
        dr_program_name = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programName').text
        dr_program_status = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}enrollmentStatus').text
        dr_program_description = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programDescription').text
        program_date1 = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programDate[1]').text
        program_date_description1 = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programDate[1]/{http://naesb.org/espi/customer}programDateDescription').text
        program_date2 = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programDate[2]').text
        program_date_description2 = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}programDate[2]/{http://naesb.org/espi/customer}programDateDescription').text
        capacity_reservation_level = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}DemandResponseProgram/{http://naesb.org/espi/customer}capacityReservationLevel').text
        pricing_structure = entry.find('.//{http://naesb.org/espi/customer}CustomerAgreement/{http://naesb.org/espi/customer}PricingStructure').text

        customer_agreement = {
            'CustomerAgreementID': customer_agreement_id,
            'CustomerID': customer_id,
            'Name': name,
            'Type': agreement_type,
            'CreatedDateTime': created_datetime,
            'LastModifiedDateTime': last_modified_datetime,
            'Email1': email1,
            'SignDate': sign_date,
            'ValidityIntervalDuration': validity_interval_duration,
            'ValidityIntervalStart': validity_interval_start,
            'IsPrePay': is_pre_pay,
            'DemandResponseProgramName': dr_program_name,
            'DemandResponseProgramStatus': dr_program_status,
            'ProgramDescription': dr_program_description,
            'ProgramDate1': program_date1,
            'ProgramDateDescription1': program_date_description1,
            'ProgramDate2': program_date2,
            'ProgramDateDescription2': program_date_description2,
            'CapacityReservationLevel': capacity_reservation_level,
            'PricingStructure': pricing_structure
        }

        customer_agreements.append(customer_agreement)

    return customer_agreements

# Function to write CustomerAgreement data to SQL Server
def write_customer_agreement_to_sql(customer_agreements):
    conn = pyodbc.connect('DRIVER={SQL Server};'
                          'SERVER=your_server;'
                          'DATABASE=your_database;'
                          'UID=your_username;'
                          'PWD=your_password')

    cursor = conn.cursor()

    for agreement in customer_agreements:
        cursor.execute('''
            INSERT INTO CustomerAgreement (CustomerAgreementID, CustomerID, Name, Type, CreatedDateTime, LastModifiedDateTime,
                                           Email1, SignDate, ValidityIntervalDuration, ValidityIntervalStart, IsPrePay,
                                           DemandResponseProgramName, DemandResponseProgramStatus, ProgramDescription,
                                           ProgramDate1, ProgramDateDescription1, ProgramDate2, ProgramDateDescription2,
                                           CapacityReservationLevel, PricingStructure)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            agreement['CustomerAgreementID'], agreement['CustomerID'], agreement['Name'], agreement['Type'],
            agreement['CreatedDateTime'], agreement['LastModifiedDateTime'], agreement['Email1'], agreement['SignDate'],
            agreement['ValidityIntervalDuration'], agreement['ValidityIntervalStart'], agreement['IsPrePay'],
            agreement['DemandResponseProgramName'], agreement['DemandResponseProgramStatus'],
            agreement['ProgramDescription'], agreement['ProgramDate1'], agreement['ProgramDateDescription1'],
            agreement['ProgramDate2'], agreement['ProgramDateDescription2'], agreement['CapacityReservationLevel'],
            agreement['PricingStructure']
        )

    conn.commit()
    conn.close()

# Usage
customer_agreements_data = parse_customer_agreement('path_to_customer_agreement.xml')
write_customer_agreement_to_sql(customer_agreements_data)
