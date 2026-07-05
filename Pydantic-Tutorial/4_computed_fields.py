from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float #kg
    height: float #mts
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculated_bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('BMI:- ', patient.calculated_bmi)
    print('inserted into database')
    


patient_info = {'name': 'Visha', 'age': 80, 'email': 'gaurav@hdfc.com', 'married': True, 'allergies': ['pollen', 'dust'], 'weight': '75.2', 'height': '1.72', 'contact_details': {'email': 'gaurav@hdfc.com', 'phone': '9876543210', 'emergency': '99999'}}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)