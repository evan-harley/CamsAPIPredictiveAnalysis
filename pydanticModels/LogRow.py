from beanie import Document, Indexed, init_beanie
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4



class LogRow(Document):
    id: UUID = Field(default_factory=uuid4)
    time: datetime
    cameraViewId: int
    camName: str
    caption: str
    latitude: float
    longitude: float
    lastAttemptTime: datetime
    lastAttemptResponseTime: int
    updatePeriodMean: float
    updatePeriodStdDev: float
    markedStale: bool
    markedDelayed: bool