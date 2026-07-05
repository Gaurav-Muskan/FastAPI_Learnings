from pydantic import BaseModel
from typing import List, Dict, Optional

class Patient(BaseModel):

     name: str
     age: int
     weight: float
    #  default value for married is added.
     married: bool = False
     allergies: Optional[List[str]] = None
     contact_details: Dict[str, str]


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    # default values will be shown for married
    print(patient.married)
    print(patient.allergies)
    print('inserted into database')
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('Updated in database')

patient_info = {'name': 'Visha', 'age': 25, 'weight': 75.2, 'contact_details': {'email': 'gaurav@gmail.com', 'phone': '9876543210'}}
patient1 = Patient(**patient_info)

insert_patient_data(patient1)