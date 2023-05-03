from datetime import datetime

from beanie import Document, TimeSeriesConfig, Granularity
from pydantic import Field


class Timeseries(Document):
    ts: datetime = Field(default_factory=datetime.now)
    camName: str
    responseTime: int
    markedStale: bool
    markedDelayed: bool


    class Settings:
        timeseries = TimeSeriesConfig(
            time_field="ts", #  Required
            meta_field="camName", #  Optional
            granularity=Granularity.minutes, #  Optional
        )