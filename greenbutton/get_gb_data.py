# get_gb_data.py
import logging
import os
import tempfile
import numpy as np
import pandas as pd
import requests
from datetime import datetime, timedelta, timezone
import xml.etree.ElementTree as ET

#import azure.functions as func
#from ..sharedcode.sftp_file_transfer import SftpFileTransfer
#from ..sharedcode.sql_conn import SqlConn
#from ..sharedcode.msgraph_sharepoint import MsGraphApiSharePoint, SharePointCredentials
# Configure the logging
logging.basicConfig(level=logging.INFO)
# Disable SSL verification (not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

class GbGetData:
    '''
    Usage:
            from .get_gb_data import GbGetData
            gbd = GbGetData()
            gbd.process_updates()
            -- or --
            with GbGetData() as gbd:
                gbd.process_updates()

            TODO: Cleanup sequencing using def functions and allow re-running, 
                  picking up where sequence left off after problem is fixed. 
    '''

    def __enter__(self):
        logging.debug(" Entering GbGetData")
        return self

    def __exit__(self, *exc_info):
        logging.debug(" Leaving GbGetData")

    def get_data(self, start_time, end_time):
        # Custom Greenbutton Dounload function
        #api_token = os.getenv("HTTP_OAUTH_TOKEN")
        api_token = "b56914a5-27fd-4bbf-b6e8-1d2176098323"
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Accept': 'application/atom+xml',
        }
        params = {
            'start': start_time,
            'end': end_time,
            'measurement-type': 'ELECTRIC',
        }
        #user_id = os.getenv("HTTP_USER_ID")
        user_id = "68b93a05-ee49-4f01-a7a8-8abaac817688"
        host = "https://naapi2-read.bidgely.com"
        api_path = f"/v2.0/dashboard/users/{user_id}/gb-download"
        url = f"{host}{api_path}"
        try:
            logging.info(f" Making a GET request")
            logging.debug(f"  to {url} with params: {params} and headers: {headers}")
            response = requests.get(url, headers=headers, params=params, verify=False)
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                return response.text
            else:
                # If the request was not successful, raise an exception
                response.raise_for_status()
        except requests.exceptions.RequestException as err:
            logging.exception(f" Error: {err}")
            return None

    def parse_xml(self, xml_text):
        if xml_text == None:
            return None
        try:
            # Parse the XML text
            tree = ET.fromstring(xml_text)

            # Now you can navigate through the XML structure
            # For example, let's print the text content of each 'element' node
            for element_node in tree.findall('.//element'):
                logging.debug(f" Element Text: {element_node.text}")

            # You can access attributes as well, for example:
            # attribute_value = tree.find('.//element').get('attribute_name')

        except ET.ParseError as err:
            logging.exception(f" XML Parse Error: {err}")
            return None
    
    def get_epoch_time_range_for_bidgely(self, start_time=None, end_time=None):
        # Get latest data if no start_time provided 
        if start_time == None:
            # Default to the current local time
            current_time = datetime.now()
            # Set the time to midnight for the current day
            start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
            # Adjust for Ameren -> Bigely Update Frequency (2 days behind current day)
            start_time = start_of_day - timedelta(days=2)

            # Set the timezone information for the datetime object
            # NOTE: Bidgely/Ameren do not properly handle time zones, so we 
            #       have to 'Set' here instead of 'Convert' the time zone.
            # Convert local datetime to UTC
            #start_time_utc = start_of_day.astimezone(timezone.utc)      
            # Set local datetime to UTC
            start_time_utc = start_time.replace(tzinfo=timezone.utc)
            # Set the time to the end of the day (23:59:59.999999)
            end_time_utc = start_time_utc + timedelta(days=1, microseconds=-1)
        else:
            # Set the timezone information for the datetime object
            # NOTE: Bidgely/Ameren do not properly handle time zones, so we 
            #       have to 'Set' here instead of 'Convert' the time zone.
            # Convert local datetime to UTC
            #start_time_utc = start_of_day.astimezone(timezone.utc)      
            # Set local datetime to UTC
            start_time_utc = start_time.replace(tzinfo=timezone.utc)
            if end_time == None:
                # Set the time to the end of the day (23:59:59.999999)
                end_time_utc = start_time_utc + timedelta(days=1, microseconds=-1)
            else:
                end_time_utc = end_time.replace(tzinfo=timezone.utc)

        # Convert datetime objects to epoch time
        start_epoch_time = int(start_time_utc.timestamp())
        end_epoch_time = int(end_time_utc.timestamp())

        logging.debug(f" Start: {start_epoch_time}, End: {end_epoch_time}")
        return start_epoch_time, end_epoch_time
    
    def save_data_to_file(self, data):
        if data == None:
            return
        try:
            # Generate a filename based on current time and date
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"gbdata_{current_time}.xml"

            # Open the file in write mode ('w')
            with open(file_path, 'w') as file:
                # Write the data to the file
                file.write(data)
            logging.info(f" Data saved to {file_path} successfully.")
        except Exception as e:
            logging.exception(f" Error saving data to file: {e}")

    def update_database(self, df):
        if df == None:
            return
        sql_server = os.getenv("SQL_SERVER")
        sql_database = os.getenv("SQL_DATABASE")
        sql_cnxn = SqlConn(sql_server, sql_database)
        sql_cnxn.connect_to_database()

        # Update tables
        logging.info("Updating Mission Control table")
        logging.info(f"File Name for Mission Control: {remote_DNC_filename}")

        # Insert into mission control
        sp_exec = """SET NOCOUNT ON; EXEC mc.usp_missioncontrol_add
                            @source_type = ?
                            , @source_name = ?
                            , @source_description = ?
                            , @source_file_name = ?
                            , @source_file_path = ?"""

        sp_params = ( 'Weekly DNC File'                      # source type
                    , remote_DNC_filename                    # source name
                    , 'Weekly DNC File'                      # source desc
                    , remote_DNC_filename                    # source file name
                    , local_file_path                        # source file path
                    )

        # open cursor run mission control procedure
        sql_cnxn.execute_sql(sp_exec,sp_params)

        # find latest mission control id
        qry_latest_mc = """ SELECT MAX(mission_control_id)
                            FROM mc.mission_control 
                            where source_type = 'Weekly DNC File'"""
        latest_mc = sql_cnxn.execute_sql_fetch_val(qry_latest_mc)
        logging.info(f'Mission Control: {latest_mc}')
        
         # instert csv data into landing.member_DNC_exclusions 
        logging.info('starting to insert data into landing.member_DNC_exclusions')
        for index,row in df.iterrows():
            query = "INSERT INTO landing.member_DNC_exclusions(mission_control_id,medicaid_region,[group],market,benefit_plan,subscriberid,medicaid_number,phone1,phone1_dnc_flag,phone1_cell_flag,phone2,phone2_dnc_flag,phone2_cell_phone_indicator,phone3,phone3_dnc_flag,phone3_cell_phone_indicator,phone4,phone4_dnc_flag,phone4_cell_phone_indicator,phone5,phone5_dnc_flag,phone5_cell_phone_indicator,eligibility_indicator,effective_date)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            params = (int(latest_mc)
                ,row.medicaid_region
                ,row.group
                ,row.market
                ,row.benefit_plan
                ,row.subscriberid
                ,row.medicaid_number
                ,row.phone1
                ,row.phone1_dnc_flag
                ,row.phone1_cell_flag
                ,row.phone2
                ,row.phone2_dnc_flag
                ,row.phone2_cell_phone_indicator
                ,row.phone3
                ,row.phone3_dnc_flag
                ,row.phone3_cell_phone_indicator
                ,row.phone4
                ,row.phone4_dnc_flag
                ,row.phone4_cell_phone_indicator
                ,row.phone5
                ,row.phone5_dnc_flag
                ,row.phone5_cell_phone_indicator
                ,row.eligibility_indicator
                ,row.effective_date
            )
            sql_cnxn.execute_sql(query, params)

        logging.info('inserted data into landing table')

        # run stored proc to 
        logging.info('starting stored procs')

        uspMemberDNCExclusionProc = """SET NOCOUNT ON; EXEC staging.usp_member_DNC_exclusions_processing @mission_control_id = ?"""
        sql_cnxn.execute_sql(uspMemberDNCExclusionProc, latest_mc)
        logging.info('completed store proc staging.usp_member_DNC_exclusions_processing')

        # End Database operations
        sql_cnxn.close_connection()

    def process_updates(self):
        logging.info(" GB Data Processing Started!")
        # Retrieve new GB Data for processing        
        #gbdata_starttime_epoch, gbdata_endtime_epoch = self.get_epoch_time_range_for_bidgely(start_time=datetime(2023, 11, 8),end_time=datetime(2023, 11, 10,23,59,59))
        gbdata_starttime_epoch, gbdata_endtime_epoch = self.get_epoch_time_range_for_bidgely()
        gb_xml_data = self.get_data(gbdata_starttime_epoch, gbdata_endtime_epoch)
        # Save data to temperary file
        self.save_data_to_file(gb_xml_data)
        # Parse GB Data
        pd = self.parse_xml(gb_xml_data)

        # Database Operations
        #self.update_database(pd)

        logging.info(" GB Data Processing Complete!")
        
        
if __name__ == '__main__':
    with GbGetData() as gbd:
        gbd.process_updates()
