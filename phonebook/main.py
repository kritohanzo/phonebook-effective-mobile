import json
from typing import Union
from models.models import Record
from utils.exceptions import ValidationError, NoMorePages, InvalidPage
from db.tools import DatabaseTools


main_menu_commands = ['1. Посмотреть все записи', '2. Добавить новую запись', '3. Найти пользователя', '0. Закрыть справочник']
find_commands = ["1. Фамилия", "2. Имя", "3. Отчество", "4. Название организации", "5. Рабочий телефон", "6. Личный телефон", "0. Начать поиск"]

def show_records(phonebook):
    while True:
        print(phonebook)
        print(phonebook.possible_commands())
        command = input("Введите номер действия: ")
        if command == '1':
            phonebook.next_page()
        elif command == '2':
            phonebook.back_page()
        elif command == '0':
            break

def configure_find_query():
    find_query = dict()
    current_find_commands = find_commands.copy()
    while True:
        print("\n".join(current_find_commands))
        command = input("Укажите параметр, по которому вы хотите искать: ")
        if command == "1":
            find_query['surname'] = input("Введите фамилию: ")
            current_find_commands.remove("1. Фамилия")
        elif command == "2":
            find_query['name'] = input("Введите имя: ")
            current_find_commands.remove("2. Имя")
        elif command == "3":
            find_query['patronymic'] = input("Введите отчество: ")
            current_find_commands.remove("3. Отчество")
        elif command == "4":
            find_query['organization_name'] = input("Введите название организации: ")
            current_find_commands.remove("4. Название организации")
        elif command == "5":
            find_query['work_phone'] = input("Введите рабочий телефон: ")
            current_find_commands.remove("5. Рабочий телефон")
        elif command == "6":
            find_query['personal_phone'] = input("Введите личный телефон: ")
            current_find_commands.remove("6. Личный телефон")
        elif command == "0":
            return find_query
        
def create_new_record():
    try:
        data = Record(surname=input('Введите фамилию: '), name=input('Введите имя: '), patronymic=input('Введите отчество: '), organization_name=input('Введите название огранизации: '), work_phone=input('Введите рабочий телефон: '), personal_phone=input('Введите личный телефон: '))
    except ValidationError as error:
        print(error)
        create_new_record()
    DatabaseTools.add_new_record(data)

def main():
    while True:
        print("\n".join(main_menu_commands))
        command = input("Введите номер действия: ")
        if command == '1':
            phonebook = DatabaseTools.get_phonebook()
            show_records(phonebook)
        elif command == '2':
            create_new_record()
        elif command == '3':
            find_query = configure_find_query()
            phonebook = DatabaseTools.find_record(find_query)
            if phonebook:
                show_records(phonebook)
            else:
                print('Записи не найдены')
        elif command == "0":
            break

if __name__ == "__main__":
    DatabaseTools.check_exists_database_file()
    main()