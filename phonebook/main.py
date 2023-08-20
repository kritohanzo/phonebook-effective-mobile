import json
from typing import Union
from models.models import Record
from utils.exceptions import ValidationError, NoMorePages, InvalidPage
from db.tools import DatabaseTools


main_menu_commands = ['1. Посмотреть все записи', '2. Добавить новую запись', '3. Найти пользователя', "4. Отредактировать существующую запись", '0. Закрыть справочник']
find_commands = ["1. Фамилия", "2. Имя", "3. Отчество", "4. Название организации", "5. Рабочий телефон", "6. Личный телефон", "0. Начать поиск"]

def edit_record():
    id = int(input("Введите ID записи, которую хотите изменить: "))
    edit_query = dict()
    # = find_commands.copy()
    while True:
        print("\n".join(find_commands))
        command = input("Укажите параметр, который вы хотите изменить: ")
        if command == "1":
            edit_query['surname'] = input("Новая фамилия: ")
        elif command == "2":
            edit_query['name'] = input("Новое имя: ")
        elif command == "3":
            edit_query['patronymic'] = input("Новое отчество: ")
        elif command == "4":
            edit_query['organization_name'] = input("Новое название организации: ")
        elif command == "5":
            edit_query['work_phone'] = input("Новый рабочий телефон: ")
        elif command == "6":
            edit_query['personal_phone']= input("Новый личный телефон: ")
        elif command == "0":
            DatabaseTools.edit_record(id, edit_query)
            break

def show_records(phonebook):
    while True:
        print('\n')
        max_columns = [] # список максимальной длинны колонок
        for col in zip(*[record.__dict__.values() for record in phonebook.current_page()]):
            len_el = []
            [len_el.append(len(str(el))) for el in col]
            max_columns.append(max(len_el))

        columns = ["ID", "Фамилия", "Имя", "Отчество", "Организация", "Рабочий телефон", "Личный телефон"]
        
        max_ln = max(max_columns) if max(max_columns) > max([len(el) for el in columns]) else max([len(el) for el in columns])
        print(f" Cтраница {phonebook.page} ".center(max_ln*8, "-"))
        
        for column in columns:
            print(f'{column:{len(column)+5}}', end='')
        print()
        # печать разделителя шапки
        print(f'{"="*max_ln*8}')
        # печать тела таблицы
        for el in [record.__dict__.values() for record in phonebook.current_page()]:
            for col in el:
                print(f'{str(col):{max_ln+3}}', end='')
            print()

        print('\n')
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
        id_for_new_record = DatabaseTools.get_new_id()
        data = Record(id=id_for_new_record, surname=input('Введите фамилию: '), name=input('Введите имя: '), patronymic=input('Введите отчество: '), organization_name=input('Введите название огранизации: '), work_phone=input('Введите рабочий телефон: '), personal_phone=input('Введите личный телефон: '))
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
        elif command == '4':
            edit_record()
        elif command == "0":
            break

if __name__ == "__main__":
    DatabaseTools.check_exists_database_file()
    main()