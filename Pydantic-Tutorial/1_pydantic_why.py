

def insert_patient_data(name: str, age: int):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print('inserted into database')
    else:
        raise TypeError('Incorrect data type.')

# Type Error is added for the parameters.
insert_patient_data("Gaurav", '25') 