from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {"message": "Welcome to Hospital Management System"}


# ---------------- PATIENTS ----------------

patients = [
    {"id": 1, "name": "Aarav", "age": 35, "disease": "Fever"},
    {"id": 2, "name": "Meera", "age": 42, "disease": "Diabetes"},
    {"id": 3, "name": "Rahul", "age": 28, "disease": "Migraine"},
    {"id": 4, "name": "Ananya", "age": 50, "disease": "Blood Pressure"},
    {"id": 5, "name": "Vikram", "age": 31, "disease": "Asthma"}
]


# Display all patients
@app.get("/patients")
def get_patients():
    return patients


# Display one patient
@app.get("/patient/{patient_id}")
def get_patient(patient_id: int):

    for patient in patients:
        if patient["id"] == patient_id:
            return patient

    return {"message": "Patient not found"}


# Add patient
class Patient(BaseModel):
    name: str
    age: int
    disease: str


@app.post("/add_patient")
def add_patient(patient: Patient):

    new_patient = {
        "id": len(patients) + 1,
        "name": patient.name,
        "age": patient.age,
        "disease": patient.disease
    }

    patients.append(new_patient)

    return {
        "message": "Patient added successfully",
        "patient": new_patient
    }


# ---------------- DOCTORS ----------------

doctors = [
    {"name": "Dr. Arjun", "specialization": "General Physician"},
    {"name": "Dr. Neha", "specialization": "Endocrinologist"},
    {"name": "Dr. Rahul", "specialization": "Neurologist"},
    {"name": "Dr. Priya", "specialization": "Cardiologist"},
    {"name": "Dr. Vikram", "specialization": "Pulmonologist"}
]


# ---------------- DISEASE → DOCTOR ----------------

disease_doctor = {
    "Fever": "General Physician",
    "Diabetes": "Endocrinologist",
    "Migraine": "Neurologist",
    "Stroke": "Neurologist",
    "Blood Pressure": "Cardiologist",
    "Heart Attack": "Cardiologist",
    "Asthma": "Pulmonologist"
}


# ---------------- APPOINTMENTS ----------------

appointments = []


class Appointment(BaseModel):
    patient_id: int
    date: str


# Book appointment
@app.post("/book_appointment")
def book_appointment(request: Appointment):

    for patient in patients:

        if patient["id"] == request.patient_id:

            specialization = disease_doctor.get(patient["disease"])

            if specialization is None:
                return {
                    "message": "No suitable doctor found"
                }

            for doctor in doctors:

                if doctor["specialization"] == specialization:

                    appointment = {
                        "patient": patient["name"],
                        "disease": patient["disease"],
                        "doctor": doctor["name"],
                        "specialization": doctor["specialization"],
                        "date": request.date,
                        "status": "Booked"
                    }

                    appointments.append(appointment)

                    return {
                        "message": "Appointment booked successfully",
                        "appointment": appointment
                    }

    return {"message": "Patient not found"}


# Display appointments
@app.get("/appointments")
def get_appointments():
    return appointments


# ---------------- UPDATE PATIENT ----------------

# Name cannot be changed
class UpdatePatient(BaseModel):
    age: int
    disease: str


@app.put("/update_patient/{patient_id}")
def update_patient(patient_id: int, patient: UpdatePatient):

    for p in patients:

        if p["id"] == patient_id:

            p["age"] = patient.age
            p["disease"] = patient.disease

            return {
                "message": "Patient updated successfully",
                "patient": p
            }

    return {"message": "Patient not found"}