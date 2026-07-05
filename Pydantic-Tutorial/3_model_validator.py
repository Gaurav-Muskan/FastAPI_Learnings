from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict

class Patient(BaseModel):

    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model
    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('inserted into database')
    


patient_info = {'name': 'Visha', 'age': 80, 'email': 'gaurav@hdfc.com', 'married': True, 'allergies': ['pollen', 'dust'], 'weight': '75.2', 'contact_details': {'email': 'gaurav@hdfc.com', 'phone': '9876543210', 'emergency': '99999'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
