# Function to parse ElectricPowerQualitySummary from Green Button XML
def parse_power_quality_summary(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    power_quality_summaries = []

    for entry in root.findall('.//{http://www.w3.org/2005/Atom}entry'):
        usage_point_id = entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}summaryInterval/{http://naesb.org/espi}start').text
        flicker_plt = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}flickerPlt').text)
        flicker_pst = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}flickerPst').text)
        harmonic_voltage = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}harmonicVoltage').text)
        long_interruptions = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}longInterruptions').text)
        mains_voltage = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}mainsVoltage').text)
        measurement_protocol = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}measurementProtocol').text)
        power_frequency = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}powerFrequency').text)
        rapid_voltage_changes = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}rapidVoltageChanges').text)
        short_interruptions = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}shortInterruptions').text)
        summary_interval_duration = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}summaryInterval/{http://naesb.org/espi}duration').text)
        summary_interval_start = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}summaryInterval/{http://naesb.org/espi}start').text)
        supply_voltage_dips = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}supplyVoltageDips').text)
        supply_voltage_imbalance = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}supplyVoltageImbalance').text)
        supply_voltage_variations = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}supplyVoltageVariations').text)
        temp_overvoltage = int(entry.find('.//{http://naesb.org/espi}ElectricPowerQualitySummary/{http://naesb.org/espi}tempOvervoltage').text)
        published = entry.find('.//{http://www.w3.org/2005/Atom}published').text
        updated = entry.find('.//{http://www.w3.org/2005/Atom}updated').text

        power_quality_summaries.append({
            'UsagePointID': usage_point_id,
            'FlickerPlt': flicker_plt,
            'FlickerPst': flicker_pst,
            'HarmonicVoltage': harmonic_voltage,
            'LongInterruptions': long_interruptions,
            'MainsVoltage': mains_voltage,
            'MeasurementProtocol': measurement_protocol,
            'PowerFrequency': power_frequency,
            'RapidVoltageChanges': rapid_voltage_changes,
            'ShortInterruptions': short_interruptions,
            'SummaryIntervalDuration': summary_interval_duration,
            'SummaryIntervalStart': summary_interval_start,
            'SupplyVoltageDips': supply_voltage_dips,
            'SupplyVoltageImbalance': supply_voltage_imbalance,
            'SupplyVoltageVariations': supply_voltage_variations,
            'TempOvervoltage': temp_overvoltage,
            'Published': published,
            'Updated': updated
        })

    return pd.DataFrame(power_quality_summaries)

# Load ElectricPowerQualitySummary data into Pandas DataFrame
power_quality_summary_data = parse_power_quality_summary('green_button_data.xml')

# Write ElectricPowerQualitySummary data to SQL Server table
power_quality_summary_data.to_sql('ElectricPowerQualitySummary', con=engine, if_exists='replace', index=False)
