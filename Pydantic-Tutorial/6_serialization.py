from pydantic import BaseModel

class Address (BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str = 'Male'
    age: int
    address: Address



address_dict = {'city': 'Patna', 'state': 'Bihar', 'pin': '800101'}

address1 = Address(**address_dict)

patient = {'name': 'Visha', 'age': 26, 'address': address1}

patient1 = Patient(**patient)


# temp = patient1.model_dump()
# temp = patient1.model_dump_json()
# temp = patient1.model_dump_json(include=['name'])
# temp = patient1.model_dump_json(exclude={'address':['state']})
# temp = patient1.model_dump_json(exclude={'address':['state']})
temp = patient1.model_dump(exclude_unset=True)

print(temp)
print(type(temp))

