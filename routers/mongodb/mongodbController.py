from fastapi import Depends, HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from database import Patients
from schema import PatientSchema
from serializers.patientSerializers import patientList, patientEntity

router = APIRouter()


@router.get("/")
def get_patients():
    patients = patientList(Patients.find())
    return patients


@router.get("/{id}")
def get_patient(id: str) -> dict:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id")

    is_patient_exists = Patients.find_one({"_id": ObjectId(id)})

    if not is_patient_exists:
        return {"error": "Patient not found"}

    return patientEntity(is_patient_exists)


@router.post("/")
def create_patient(patient: PatientSchema) -> Response:
    try:
        new_patient = Patients.insert_one(patient.dict())
        return Response(status_code=status.HTTP_201_CREATED,
                        content=f"Patient created with id: {new_patient.inserted_id}")
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient already exists")


@router.put("/{id}")
def update_patient(id: str, payload: PatientSchema) -> Response:
    is_patient_exists = Patients.find_one({"_id": ObjectId(id)})
    if not is_patient_exists:
        return {"error": "Patient not found"}

    Patients.find_one_and_update(
        {"_id": ObjectId(id)},
        {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    return {"message": "Patient updated"}


@router.delete("/{id}")
def delete_patient(id: str) -> Response:
    is_patient_exists = Patients.find_one({"_id": ObjectId(id)})
    if not is_patient_exists:
        return {"error": "Patient not found"}

    Patients.delete_one({"_id": ObjectId(id)})
    return {"message": "Patient deleted successfully"}
