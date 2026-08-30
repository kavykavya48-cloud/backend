from pydantic import BaseModel
from typing import Optional


class EmergencyReport(BaseModel):
    emergency_type: str
    description: str
    location: Optional[str] = None


class EmergencyResponse(BaseModel):
    emergency_id: str
    emergency_type: str
    description: str
    location: Optional[str] = None
    status: str
    