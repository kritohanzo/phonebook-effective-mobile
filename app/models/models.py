from utils.exceptions import ValidationError

class Record:
    def __init__(self, surname: str, name: str, patronymic: str, orgranizaton_name: str, work_phone: str, personal_phone: str):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.orgranizaton_name = orgranizaton_name
        self.work_phone = work_phone
        self.personal_phone = personal_phone
        # self.validate()

    # def validate(self):
    #     if not self.first_name and not self.last_name:
    #         raise ValidationError("Одно из полей first_name или last_name должно быть заполнено.")
    
    # def dict(self):
    #     return {"first_name": self.first_name, "last_name": self.last_name, "number": self.number}