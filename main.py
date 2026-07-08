from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
import tkinter as tk
from tkinter import messagebox

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field( ... , description='ID of the patient', examples=['P001' ] )]
    name: Annotated[str, Field( ... , description='Name of the patient')]
    city: Annotated[str, Field( ... , description='City where the patient is living')]
    age: Annotated[int, Field( ... , gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2),2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


def load_data():
    with open ('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open ('patients.json','w') as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {'message':'Patient Management System API'}


@app.get("/about")
def about():
    return {'message':'A fully funcitonal API to manage your patient records'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient_data(patient_id: str = Path(..., description='ID of the patient in the DB.', examples='P001')):
    # load all Patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), 
                  order: str = Query('asc', description='sort in desc or asc order')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='Invalid fields, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc or desc')
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


 # FastAPI receives the JSON payload and passes it to the Patient-Pydantic model for parsing and validation.
@app.post('/create')
def create_patient(patient: Patient): 
    # The incoming JSON request body is automatically parsed and validated
    # against the Patient Pydantic model before this function is executed.
    
    # Load existing data
    data = load_data()
    # Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    # New patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})

@app.patch('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    # patient_update payload example (received from request body)
    # Example
    # name='Solu' city='Kolkata' age=1 gender='male' height=1.0 weight=1.0 bmi=1.0 verdict='Underweight'

    # Load all patient records from the JSON file.
    # data -> dict
    data = load_data()

    # Check whether the patient exists.
    print("Line 148 ",patient_update)
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    # Extract the existing patient information.
    # existing_patient_info -> dict
    #  Existing data:- 
    # {'name': 'Gaurav', 'city': 'Kolkata', 'age': 1, 'gender': 'male', 'height': 1.0, 'weight': 1.0, 'bmi': 1.0, 'verdict': 'Underweight'}
    existing_patient_info = data[patient_id]
    # print("Line 157 ", existing_patient_info)
    # {'name': 'Gaurav', 'city': 'Kolkata', 'age': 1, 'gender': 'male', 'height': 1.0, 'weight': 1.0, 'bmi': 1.0, 'verdict': 'Underweight'}
    # Convert the Pydantic model into a dictionary while ignoring fields that were not provided in the request.
    
    # Example:
    # patient_update (Pydantic object) We are adding {} to the incoming request
    #      ↓
    # {"city": "Patna", "weight": 80}
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    # {'name': 'Solu', 'city': 'Kolkata', 'age': 1, 'gender': 'male', 'height': 1.0, 'weight': 1.0, 'bmi': 1.0, 'verdict': 'Underweight'}
    # print("Line 167 ", updated_patient_info)
    # Iterate over the updated fields and overwrite the corresponding
    # values in the existing patient record.
    #
    # Before:
    # {"city": "Mumbai", "weight": 85}
    #
    # After:
    # {"city": "Patna", "weight": 80}
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    # The existing patient dictionary currently doesn't contain the id.
    # Add it because the Patient Pydantic model expects an id field.
    #
    # existing_patient_info
    #      ↓
    # {
    #   "id": "P002",
    #   "name": "Ravi Mehta",
    #   ...
    # }
    existing_patient_info["id"] = patient_id
    # {'name': 'Solu', 'city': 'Kolkata', 'age': 1, 'gender': 'male', 'height': 1.0, 'weight': 1.0, 'bmi': 1.0, 'verdict': 'Underweight', 'id': 'P005'}
    # print("Line 191 ", existing_patient_info)
    # Convert the updated dictionary into a Patient Pydantic object.
    #
    # dict
    #      ↓
    # Patient Pydantic object
    patient_pydantic_obj = Patient(**existing_patient_info)
    # id='P005' name='Solu' city='Kolkata' age=1 gender='male' height=1.0 weight=1.0 bmi=1.0 verdict='Underweight'
    # print("Line 199 ", patient_pydantic_obj)
    # Convert the Pydantic object back into a dictionary.
    # This recalculates computed fields like bmi and verdict.
    #
    # Patient object
    #      ↓
    # dict
    existing_patient_info = patient_pydantic_obj.model_dump()
    # {'id': 'P005', 'name': 'Solu', 'city': 'Kolkata', 'age': 1, 'gender': 'male', 'height': 1.0, 'weight': 1.0, 'bmi': 1.0, 'verdict': 'Underweight'}
    # print("Line 208 ", existing_patient_info)
    # Remove the id field before storing because the patient id
    # is already used as the dictionary key.
    existing_patient_info.pop("id")

    # Save the updated patient information back into the main dictionary.
    #
    # data["P002"]
    #      ↓
    # updated patient dictionary
    data[patient_id] = existing_patient_info

    # Persist the updated data to the JSON file.
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not find.')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'Patient deleted.'})