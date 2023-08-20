from utils.exceptions import ValidationError, NoMorePages, InvalidPage
from math import ceil

LIMIT_OF_RECORDS_ON_ONE_PAGE = 5

class Record:
    def __init__(self, id: int, surname: str, name: str, patronymic: str, organization_name: str, work_phone: str, personal_phone: str):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.organization_name = organization_name
        self.work_phone = work_phone
        self.personal_phone = personal_phone
        self.validate()

    def validate(self):
        for value in self.__dict__.values():
            if not value:
                raise ValidationError("Все поля должны быть заполнены.")
    
    def __str__(self):
        message = "[" + str(self.id) + "] " + self.surname + " " + self.name + " " + self.patronymic + " работает в организации " +  self.organization_name + ". Рабочий номер телефона: " + self.work_phone + ", личный номер телефона: " + self.personal_phone
        return message
    
class Phonebook:
    page: int = 1

    def __init__(self, records: list[Record]):
        self.records = records

    def next_page(self):
        self.page += 1
        # if self.page > ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE):
        #     raise NoMorePages
        
    def back_page(self):
        self.page -= 1
        # if self.page < 1:
        #     raise InvalidPage
        
    def possible_commands(self):
        if self.page >= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE) and self.page == 1:
            return "\n".join(["0. В главное меню"])
        if self.page >= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE) and self.page > 1:
            return "\n".join(["2. Предыдущая страница", "0. В главное меню"])
        if self.page <= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE) and self.page == 1:
            return "\n".join(["1. Следующая страница", "0. В главное меню"])
        if self.page <= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE) and self.page > 1:
            return "\n".join(["1. Следующая страница", "2. Предыдущая страница", "0. В главное меню"])
    
    def current_page(self):
        return self.records[LIMIT_OF_RECORDS_ON_ONE_PAGE*(self.page-1): LIMIT_OF_RECORDS_ON_ONE_PAGE*self.page]

    def __str__(self):
        return "\n".join(list(map(str, self.records[LIMIT_OF_RECORDS_ON_ONE_PAGE*(self.page-1): LIMIT_OF_RECORDS_ON_ONE_PAGE*self.page])))
