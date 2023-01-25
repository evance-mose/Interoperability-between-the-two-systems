from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
import model
import schema
from database import engine, SessionLocal, get_db

model.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(model.Patient).all()
    return patients


@router.get("/{id}")
def get_patient(id: int, db: Session = Depends(get_db)):
    patient = db.query(model.Patient).filter(model.Patient.id == id).first()
    if not patient:
        return {"error": "Patient not found"}

    return patient


@router.post("/")
def create_patient(patient: schema.PatientSchema, db: Session = Depends(get_db)):
    db_patient = db.query(model.Patient).filter(model.Patient.ssn == patient.ssn).first()
    if db_patient:
        raise HTTPException(status_code=400, detail="Patient already exists")
    id = db.query(model.Patient).count() + 1
    new_patient = model.Patient(id=id, ssn=patient.ssn, name=patient.name, address=patient.address, phone=patient.phone,
                                created_at=patient.created_at, updated_at=patient.updated_at)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    raise HTTPException(status_code=201, detail="Patient created")


@router.put("/{id}")
def update_patient(id: int, patient: schema.PatientSchema, db: Session = Depends(get_db)):
    db_patient = db.query(model.Patient).filter(model.Patient.id == id).first()
    if not db_patient:
        return {"error": "Patient not found"}

    db_patient.ssn = patient.ssn
    db_patient.name = patient.name
    db_patient.address = patient.address
    db_patient.phone = patient.phone
    db_patient.created_at = patient.created_at
    db_patient.updated_at = patient.updated_at
    db.commit()
    raise HTTPException(status_code=200, detail="Patient updated")


@router.delete("/{id}")
def delete_patient(id: int, db: Session = Depends(get_db)):
    db_patient = db.query(model.Patient).filter(model.Patient.id == id).first()
    if not db_patient:
        return {"error": "Patient not found"}
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
