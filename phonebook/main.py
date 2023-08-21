import logging
from pathlib import Path
from models import Record, Table, Phonebook
from db import Tools as db


def get_logger() -> logging:
    """Функция, отвечающая за создание логгера.

    Возвращает логгер,
    который записывает информационные и ошибочные события в файл.
    """
    logger = logging.getLogger("logfile")
    log_file = Path(__file__).parent / "phonebook.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    log_format = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
    file_handler.setFormatter(log_format)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    return logger


def edit_record() -> None:
    """Функция, запускающая процесс редактириования записи."""
    commands = [
        "1. Фамилия",
        "2. Имя",
        "3. Отчество",
        "4. Название организации",
        "5. Рабочий телефон",
        "6. Личный телефон",
        "7. Изменить запись",
        "0. Отмена (в главное меню)",
    ]
    id = int(input("Введите ID записи, которую хотите изменить: "))
    if not db.check_exists_id_in_database(id):
        print("Введён невалидный ID записи.")
        logger.error("Введён невалидный ID записи.")
        return
    query = dict()
    while True:
        print("\n".join(commands))
        command = input(
            "Укажите параметр, который вы хотите изменить, "
            "после чего выберите 7 для изменения "
            "или 0 для выхода в главное меню: "
        )
        if command == "1":
            query["surname"] = input("Новая фамилия: ")
        elif command == "2":
            query["name"] = input("Новое имя: ")
        elif command == "3":
            query["patronymic"] = input("Новое отчество: ")
        elif command == "4":
            query["organization_name"] = input("Новое название организации: ")
        elif command == "5":
            query["work_phone"] = input("Новый рабочий телефон: ")
        elif command == "6":
            query["personal_phone"] = input("Новый личный телефон: ")
        elif command == "7":
            db.edit_record(id, query)
            logging.info(f"Запись с ID {id} отредактирована.")
            print("Запись отредактирована")
            break
        elif command == "0":
            break


def show_records() -> None:
    """Функция, запускающая процесс показа страницы с записями."""
    phonebook = db.get_phonebook()
    while True:
        table = Table(
            [
                "ID",
                "Фамилия",
                "Имя",
                "Отчество",
                "Организация",
                "Раб. тел.",
                "Личный тел.",
            ],
            phonebook,
        )
        print(table.show_table())
        print(phonebook.possible_commands())
        command = input("Введите номер действия: ")
        if phonebook.possible_commands()[0][0] == "1" and command == "1":
            phonebook.next_page()
        elif phonebook.possible_commands()[0][0] == "2" and command == "2":
            phonebook.back_page()
        elif command == "0":
            break


def find_record() -> Phonebook:
    """Функция, запускающая процесс поиска записей."""
    commands = [
        "1. Фамилия",
        "2. Имя",
        "3. Отчество",
        "4. Название организации",
        "5. Рабочий телефон",
        "6. Личный телефон",
        "7. Начать поиск",
        "0. Отмена (в главное меню)",
    ]
    promt = dict()
    while True:
        print("\n" + "\n".join(commands))
        command = input(
            "Укажите параметр, по которому вы хотите искать, "
            "после чего выберите 7 для поиска "
            "или 0 для выхода в главное меню: "
        )
        if command == "1":
            promt["surname"] = input("Введите фамилию: ")
            commands.remove("1. Фамилия")
        elif command == "2":
            promt["name"] = input("Введите имя: ")
            commands.remove("2. Имя")
        elif command == "3":
            promt["patronymic"] = input("Введите отчество: ")
            commands.remove("3. Отчество")
        elif command == "4":
            promt["organization_name"] = input(
                "Введите название организации: "
            )
            commands.remove("4. Название организации")
        elif command == "5":
            promt["work_phone"] = input("Введите рабочий телефон: ")
            commands.remove("5. Рабочий телефон")
        elif command == "6":
            promt["personal_phone"] = input("Введите личный телефон: ")
            commands.remove("6. Личный телефон")
        elif command == "7":
            phonebook = db.find_record(promt)
            if phonebook:
                show_records(phonebook)
            else:
                print("Записи не найдены")
        elif command == "0":
            break


def create_new_record() -> None:
    """Функция, запускающая процесс создания новой записи."""
    new_id = db.get_new_id()
    try:
        record = Record(
            id=new_id,
            surname=input("Введите фамилию: "),
            name=input("Введите имя: "),
            patronymic=input("Введите отчество: "),
            organization_name=input("Введите название огранизации: "),
            work_phone=input("Введите рабочий телефон: "),
            personal_phone=input("Введите личный телефон: "),
        )
    except ValueError as error:
        print(error)
        logger.error(error)
        return
    db.add_new_record(record)
    logging.info(f"Добавлена новая запись с ID {new_id}")


def main() -> None:
    """Главная функция, точка входа в программу.

    В дальнейшем из неё будут запускаться остальные функции приложения.
    """
    logger.info("Программа запущена.")
    commands = [
        "1. Посмотреть все записи",
        "2. Добавить новую запись",
        "3. Найти пользователя",
        "4. Отредактировать существующую запись",
        "0. Закрыть справочник",
    ]

    while True:
        print("\n".join(commands))
        command = input("Введите номер действия: ")

        if command == "1":
            show_records()
        elif command == "2":
            create_new_record()
        elif command == "3":
            find_record()
        elif command == "4":
            edit_record()
        elif command == "0":
            break
    logger.info("Программа выключена с помощью меню.")


if __name__ == "__main__":
    db.check_exists_database_file()
    logger = get_logger()
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Программа выключена сочетанием CTRL + C.")
    except Exception:
        logger.warning("Произошло непредвиденное завершение программы!")
