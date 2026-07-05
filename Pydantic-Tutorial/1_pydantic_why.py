from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

     name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 Characters.', examples=["Solu", "Anit"])]
     age: int
     email: EmailStr
     linkedin_url: AnyUrl
     weight: Annotated[float, Field(gt=0, strict=True)]
    #  default value for married is added.
     married: Annotated[bool, Field(default=False, description='Is the patient married or not.')]
     allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
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

patient_info = {'name': 'Visha', 'age': 25, 'email': 'gaurav@gmail.com', 'linkedin_url': 'http://linkedin.com/visha19', 'weight': '75.2', 'contact_details': {'email': 'gaurav@gmail.com', 'phone': '9876543210'}}
patient1 = Patient(**patient_info)

insert_patient_data(patient1)