from models.models import Record, Phonebook
import json
from pathlib import Path

LIMIT_OF_RECORDS_ON_ONE_PAGE = 5

class DatabaseTools:
    filename = Path(__file__).parent / "db.json"

    @classmethod
    def check_exists_database_file(cls) -> None:
        if not cls.filename.exists():
            with open(cls.filename, 'w', encoding='utf-8') as new_file:
                json.dump([], new_file, indent=4)

    @classmethod
    def get_new_id(cls) -> int:
        with open(cls.filename, 'r', encoding='utf-8') as file:
            data = list(map(lambda x: Record(**x), json.load(file)))
        return len(data) + 1


    @classmethod
    def add_new_record(cls, record: Record) -> None:
        with open(cls.filename, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.append(record.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)

    @classmethod
    def get_phonebook(cls) -> Phonebook:
        with open(cls.filename, 'r', encoding='utf-8') as file:
            data = list(map(lambda x: Record(**x), json.load(file)))
        # for i in range(0, len(data), LIMIT_OF_RECORDS_ON_ONE_PAGE):
        #     yield data[i:i+LIMIT_OF_RECORDS_ON_ONE_PAGE]
        return Phonebook(data)
        
    @classmethod
    def find_record(cls, find_data: dict) -> Phonebook:
        result = []
        with open(cls.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for record in data:
            for field in find_data:
                if find_data[field] != record[field]:
                    break
            else:        
                result.append(Record(**record))

        if result:
            return Phonebook(result)
    
    @classmethod
    def edit_record(cls, id: int, edit_data: dict) -> None:
        with open(cls.filename, 'r+', encoding='utf-8') as file:
            data = json.load(file)
        
            for field in edit_data:
                data[id-1][field] = edit_data[field]
                
            file.seek(0)
            json.dump(data, file, indent=4)