from models.models import Record
import json

class DatabaseTools:
    filename = "db/test.json"

    @classmethod
    def add_new_record(cls, record: Record) -> None:
        with open(cls.filename, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.append(record.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)

    @classmethod
    def get_all_records(cls) -> list[Record]:
        with open(cls.filename, 'r', encoding='utf-8') as file:
            data = list(map(lambda x: Record(**x), json.load(file)))
            return data