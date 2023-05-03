import asyncio

from pydanticModels.LogRow import LogRow
from pydanticModels.TimeSeries import Timeseries
from datetime import datetime
from beanie import Document, Indexed, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import requests
from typing import List
from tqdm.auto import tqdm


async def parse_data(data: dict) -> List[LogRow]:
    records = []
    for record in data['webcams']:
        row_data = LogRow(
                    time=datetime.now(),
                    cameraViewId= record['id'],
                    cameraName= record['camName'],
                    caption= record['caption'],
                    latitude= record['location']['latitude'],
                    longitude= record['location']['longitude'],
                    lastAttemptTime= record['imageStats']['lastAttempt']['time'],
                    lastAttemptResponseTime= record['imageStats']['lastAttempt']['seconds'],
                    updatePeriodMean= record['imageStats']['updatePeriodMean'],
                    updatePeriodStdDev= record['imageStats']['updatePeriodStdDev'],
                    markedStale= record['imageStats']['markedStale'],
                    markedDelayed= record['imageStats']['markedDelayed'])

        records.append(row_data)

    return records

async def parse_timeseries(data:dict) -> List[Timeseries]:
    records = []
    for record in data['webcams']:
        row_data = Timeseries(
            ts=datetime.now,
            camName=record['camName'],
            responseTime=record['imageStats']['lastAttempt']['seconds'],
            markedStale=record['imageStats']['markedStale'],
            markedDelayed=record['imageStats']['markedDelayed']
            )
        records.append(row_data)
    return records



async def init():
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    await init_beanie(client.CameraAPIData, document_models=[LogRow])


async def get_data():
    for i in tqdm(range(2, 1018)):
        api_url = "https://images.drivebc.ca/webcam/api/v1/webcams?fields=id,camName,caption,location,imageStats"
        response = requests.get(api_url)
        if response.status_code != 200:
            continue
        else:
            log_rows = await parse_data(response.json())
            LogRow.insert_many(log_rows)
            ts_rows = await parse_timeseries(response.json())
            Timeseries.insert_many(ts_rows)

    print("All Cam Data parsed and imported")


async def main():
    await init()
    await get_data()


def run():
    asyncio.run(main())


if __name__ == '__main__':
    run()

