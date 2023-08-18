import json
from typing import Union
from models.models import Record
from db.tools import DatabaseTools



# user = User("79923080013", "as")

# with open("test.txt", "a") as file:
#     _input = User(first_name=input("Введите имя"), last_name=input("Введите фамилию"), number=input("Введите номер"))
#     file.write(json.dumps(_input.dict()))

# DatabaseTools.add_new_record(Record(surname="hanzo", name="krito", patronymic='hizovich', orgranizaton_name="Topol", work_phone="6463", personal_phone="7537323"))
data = DatabaseTools.get_all_records()
for i in data:
    print(type(i))
# with open("app/db/test.json", "r") as file:
#     text = json.load(file)
#     for i in text:
#         print(i)
