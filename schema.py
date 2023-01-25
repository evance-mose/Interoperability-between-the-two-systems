from datetime import date
from pydantic import BaseModel


class PatientSchema(BaseModel):
    ssn: str
    name: str
    address: str
    phone: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True