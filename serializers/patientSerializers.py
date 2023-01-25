from bson import ObjectId


def patientEntity(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "ssn": patient["ssn"],
        "name": patient["name"],
        "address": patient["address"],
        "phone": patient["phone"],
        "created_at": patient["created_at"],
        "updated_at": patient["updated_at"],
    }


def patientList(patients) -> list:
    return [patientEntity(patient) for patient in patients]
