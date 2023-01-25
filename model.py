from sqlalchemy import Column, Integer, String
from database import Base


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ssn = Column(String(225), unique=True)
    name = Column(String(225))
    address = Column(String(225))
    phone = Column(String(15))
    created_at = Column(String(225))
    updated_at = Column(String(225))




