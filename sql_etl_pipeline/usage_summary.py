# Function to parse UsageSummary from Green Button XML
def parse_usage_summary(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    usage_summaries = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        usage_point_id = entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}billingPeriod/{http://naesb.org/espi}start').text
        billing_period_duration = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}billingPeriod/{http://naesb.org/espi}duration').text)
        billing_period_start = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}billingPeriod/{http://naesb.org/espi}start').text)
        bill_last_period = float(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}billLastPeriod').text)
        bill_to_date = float(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}billToDate').text)
        cost_additional_last_period = float(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}costAdditionalLastPeriod').text)
        currency = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}currency').text)
        overall_consumption_last_period = float(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}overallConsumptionLastPeriod/{http://naesb.org/espi}value').text)
        overall_consumption_last_period_multiplier = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}overallConsumptionLastPeriod/{http://naesb.org/espi}powerOfTenMultiplier').text)
        overall_consumption_last_period_uom = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}overallConsumptionLastPeriod/{http://naesb.org/espi}uom').text)
        current_billing_period_overall_consumption = float(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}currentBillingPeriodOverAllConsumption/{http://naesb.org/espi}value').text)
        current_billing_period_overall_consumption_multiplier = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}currentBillingPeriodOverAllConsumption/{http://naesb.org/espi}powerOfTenMultiplier').text)
        current_billing_period_overall_consumption_timestamp = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}currentBillingPeriodOverAllConsumption/{http://naesb.org/espi}timeStamp').text)
        current_billing_period_overall_consumption_uom = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}currentBillingPeriodOverAllConsumption/{http://naesb.org/espi}uom').text)
        quality_of_reading = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}qualityOfReading').text)
        status_time_stamp = int(entry.find('.//{http://naesb.org/espi}UsageSummary/{http://naesb.org/espi}statusTimeStamp').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        usage_summaries.append({
            'UsagePointID': usage_point_id,
            'BillingPeriodDuration': billing_period_duration,
            'BillingPeriodStart': billing_period_start,
            'BillLastPeriod': bill_last_period,
            'BillToDate': bill_to_date,
            'CostAdditionalLastPeriod': cost_additional_last_period,
            'Currency': currency,
            'OverallConsumptionLastPeriod': overall_consumption_last_period,
            'OverallConsumptionLastPeriodMultiplier': overall_consumption_last_period_multiplier,
            'OverallConsumptionLastPeriodUOM': overall_consumption_last_period_uom,
            'CurrentBillingPeriodOverallConsumption': current_billing_period_overall_consumption,
            'CurrentBillingPeriodOverallConsumptionMultiplier': current_billing_period_overall_consumption_multiplier,
            'CurrentBillingPeriodOverallConsumptionTimestamp': current_billing_period_overall_consumption_timestamp,
            'CurrentBillingPeriodOverallConsumptionUOM': current_billing_period_overall_consumption_uom,
            'QualityOfReading': quality_of_reading,
            'StatusTimeStamp': status_time_stamp,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(usage_summaries)

# Load UsageSummary data into Pandas DataFrame
usage_summary_data = parse_usage_summary('green_button_data.xml')

# Write UsageSummary data to SQL Server table
usage_summary_data.to_sql('UsageSummary', con=engine, if_exists='replace', index=False)
