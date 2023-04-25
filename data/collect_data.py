
from datetime import datetime
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
import os
import pandas as pd
import requests
import schedule
import time

def collect_data(db_client: InfluxDBClient):
    api_url = "https://images.drivebc.ca/webcam/api/v1/webcams?fields=id,camName,caption,location,imageStats"
    response = requests.get(api_url)
    data = parse_data(response.json())
    bucket = 'BC_HighwayCamData'
    with db_client.write_api() as write_client:
        write_client.write(bucket, 'Base45', data)

def parse_data(data: dict) -> dict:
    records = []
    for record in data['webcams']:
        row_data = {
            'measurement': record['camName'],
            'time': datetime.now(),        
            'tags': {
                'cameraViewId': record['id'],  
                'caption': record['caption'],
                'latitude': record['location']['latitude'],
                'longitude': record['location']['longitude'],
                'elevation': record['location']['elevation']},
            'fields':{
                'lastAttemptTime': record['imageStats']['lastAttempt']['time'],
                'lastAttemptResponseTime': record['imageStats']['lastAttempt']['seconds'],
                'updatePeriodMean': record['imageStats']['updatePeriodMean'],
                'updatePeriodStdDev': record['imageStats']['updatePeriodStdDev'],
                'markedStale': record['imageStats']['markedStale'],
                'markedDelayed': record['imageStats']['markedDelayed']}
                }
        records.append(row_data)

    return records

def main():
    load_dotenv()
    client = InfluxDBClient(url='https://influx.base45.ca', org='Base45', token=os.getenv('token'))
    collect_data(client)
    print(f'Data Collected @ {datetime.now()}')


if __name__ == '__main__':

    print("Data Collection in Progress.")
    schedule.every(2).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

