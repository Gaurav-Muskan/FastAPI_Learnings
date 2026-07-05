from pydantic import BaseModel

class Patient(BaseModel):

     name: str
     age: int


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('inserted into database')
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('Updated in database')

patient_info = {'name': 'Visha', 'age': 25}
patient1 = Patient(**patient_info)

# insert_patient_data(patient1)
update_patient_data(patient1)