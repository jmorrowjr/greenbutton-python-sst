import sys
import pandas as pd
from parse import parse_feed
from pytz import timezone

ups = parse_feed(sys.argv[1])


company_rate_plans = {
    "AnyTime Users": {'time_periods': [(0, 24)], 'threshold': [750], 'rates': [0.093, 0.063], 'total_usage': 0},
    "Ultimate Savers": {'time_periods': [(0, 6), (6, 8), (8, 18), (18, 20), (20, 24)], 'rates': [0.051, 0.3, 0.051, 0.3, 0.051], 'demand_charge': 3.37, 'demand_hours': (6, 22), 'total_usage': 0, 'highest_usage': 0},
    "Morning/Evening Savers": {'time_periods': [(0, 9), (9, 21), (21, 24)], 'threshold': [750], 'rates': [0.092, 0.062, 0.094, 0.064, 0.092, 0.062], 'total_usage': 0},
    "Overnight Savers": {'time_periods': [(0, 6), (6, 22), (22, 24)], 'rates': [0.056, 0.091, 0.056], 'total_usage': 0},
    "Smart Savers": {'time_periods': [(0, 6), (6, 8), (8, 18), (18, 20), (20, 22), (22, 24)], 'rates': [0.056, 0.191, 0.068, 0.191, 0.068, 0.056], 'total_usage': 0}
}

# Function to calculate cost for each row in the DataFrame
def calculate_cost(row):
    datetime_usage = row['Datetime']
    kWh_usage = row['kWh_usage']
    total_cost = {plan: calculate_energy_cost(plan, datetime_usage, kWh_usage) for plan in company_rate_plans}
    return pd.Series(total_cost)


def calculate_energy_cost(rate_plan, datetime_usage, kWh_usage):
    # Retrieve rate plan details
    plan_details = company_rate_plans.get(rate_plan)
    # Extract hour and minute from datetime
    hour, minute = datetime_usage.hour, datetime_usage.minute

    # Initialize total usage if not present
    total_usage = 0
    if 'total_usage' in plan_details:
        total_usage = plan_details['total_usage']

    time_period_index = 0
    for time_period in plan_details['time_periods']:
        start_hour, end_hour = time_period
        if start_hour <= hour < end_hour:
            # Check for kWh threshold
            if 'threshold' in plan_details:
                threshold_index = (time_period_index * 2)
                if total_usage < plan_details['threshold'][0]:
                    rate = plan_details['rates'][threshold_index]
                else:
                    rate = plan_details['rates'][threshold_index+1]
            else:
                rate = plan_details['rates'][time_period_index]
            
            # Need to extract highest usage hour for the month
            if 'demand_charge' in plan_details:
                demand_start_hour, demand_end_hour = plan_details['demand_hours']
                if demand_start_hour <= hour <= demand_end_hour:
                    if 'highest_usage' in plan_details:
                        highest_usage = plan_details['highest_usage']
                        if highest_usage < kWh_usage:
                            highest_usage = kWh_usage
                            # Update total usage in the rate plan details
                            plan_details['highest_usage'] = kWh_usage

            cost = kWh_usage * rate

            '''
            # Check for demand charge
            if 'demand_charge' in plan_details:
                # Need to extract highest usage hour for the month
                demand_start_hour, demand_end_hour = plan_details['demand_hours']
                highest_usage_hour = max(datetime_usage, key=lambda x: x.hour)
                demand_charge_hour = highest_usage_hour.hour

                if demand_start_hour <= demand_charge_hour <= demand_end_hour:
                    # May need to subtract
                    cost += (kWh_usage * plan_details['demand_charge'])
            '''
            # Update total usage
            total_usage += kWh_usage
            
            # Update total usage in the rate plan details
            plan_details['total_usage'] = total_usage

            return cost
        time_period_index += 1

for up in ups:
    print('UsagePoint (%s) %s %s:' % (up.title, up.serviceCategory.name, up.status))
    for mr in up.meterReadings:
        print('  Meter Reading (%s) %s:' % (mr.title, mr.readingType.uom.name))
        # Create a list of lists based on the 'ir' data
        #data_list = [[ir.timePeriod.start, ir.timePeriod.duration, ir.value, ir.value_symbol] for ir in mr.intervalReadings]
        data_list = [[ir.timePeriod.start, ir.value/1000.0] for ir in mr.intervalReadings]

        # Convert the list into a Pandas DataFrame
        #df = pd.DataFrame(data_list, columns=['Datetime', 'Duration', 'Value', 'Value_Symbol'])
        df = pd.DataFrame(data_list, columns=['Datetime', 'kWh_usage'])

        # Convert UTC to CDT (Central Daylight Time)
        #central = timezone('US/Central')  # Set the timezone to CDT
        #df['cdt_datetime'] = df['utc_datetime'].dt.tz_convert(central)

        # Remove the timezone information from the column
        #df['Datetime'] = df['Datetime'].dt.tz_localize(None)

        # Extract the time component from the DateTimeInterval and convert it to a string
        #df['Duration'] = df['Duration'].dt.components['minutes'].astype(str) + ':' + df['Duration'].dt.components['seconds'].astype(str)


        # Now 'df' contains the Pandas DataFrame with the collected data
        #print(df)
        #df.to_csv("greenbutton_parse.csv", index=False)
        #for ir in mr.intervalReadings:
        #    print('    %s, %s, %s, %s' % (ir.timePeriod.start, ir.timePeriod.duration, ir.value, ir.value_symbol), end='\n')
        #    if ir.cost is not None:
        #        print(' (%s%s)' % (ir.cost_symbol, ir.cost))
            #if len(ir.readingQualities) > 0:
            #    logging.info('[%s]' % ', '.join([rq.quality.name for rq in ir.readingQualities]))
            #logging.info

        # Apply the calculate_cost function to each row and concatenate the results into a new DataFrame
        result_df = pd.concat([df, df.apply(calculate_cost, axis=1)], axis=1)
        plan_details = company_rate_plans.get('Ultimate Savers')
        if 'highest_usage' in plan_details:
            highest_usage = plan_details['highest_usage']
            # Check for demand charge
            if 'demand_charge' in plan_details:
                # May need to subtract
                demand_charge = (highest_usage * plan_details['demand_charge'])
                print(f"Ultimate Savers Demand charge: ${demand_charge}\n")

        # Display the resulting DataFrame
        print(result_df)
        result_df.to_csv("energyoptimate_parse_231204.csv", index=False)



