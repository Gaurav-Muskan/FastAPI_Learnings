from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    age: int
    email: EmailStr
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # Checking  whether email belongs to hdfc or icici
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        print(value)
        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    # Mode is used to get value before type coersion.
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):

        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 to 100')

    # Converting name to Upper Case.
    @field_validator('name', mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('inserted into database')
    

patient_info = {'name': 'Visha', 'age': 25, 'email': 'gaurav@hdfc.com', 'married': True, 'allergies': ['pollen', 'dust'], 'weight': '75.2', 'contact_details': {'email': 'gaurav@hdfc.com', 'phone': '9876543210'}}

patient1 = Patient(**patient_info) # Validation & Type coersion takes place at this place.

insert_patient_data(patient1)