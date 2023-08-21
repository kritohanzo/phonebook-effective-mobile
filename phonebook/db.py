import json
from pathlib import Path
from models import Record, Phonebook


class Tools:
    """Класс для работы с базой данных в формате JSON.

    Предоставляет методы для создания базы данных, получения
    нового ID для записи, добавления записи в JSON-файл,
    получения объекта модели Phonebook, поиска записей в объекте модели,
    проверки данных на наличие нужного ID в базе и редактирования записей.
    """

    filename = Path(__file__).parent / "db.json"

    @classmethod
    def check_exists_database_file(cls) -> None:
        """Метод для проверки наличия базы данных.

        Проверяет наличие созданной базы данных в виде JSON-файла,
        создаст её самостоятельно, если она отсутствует.
        """
        if not cls.filename.exists():
            with open(cls.filename, "w", encoding="utf-8") as new_file:
                json.dump([], new_file, indent=4)

    @classmethod
    def get_new_id(cls) -> int:
        """Метод для выдачи нового ID.

        Выдаёт новый ID для записи,
        в зависимости от загруженности базы данных.
        """
        with open(cls.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return len(data) + 1

    @classmethod
    def add_new_record(cls, record: Record) -> None:
        """Метод для добавления новой записи в базу данных."""
        with open(cls.filename, "r+", encoding="utf-8") as file:
            data = json.load(file)
            data.append(record.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)

    @classmethod
    def get_phonebook(cls) -> Phonebook:
        """Метод для получения телефонного справочника.

        Возвращает объект модели Phonebook,
        в которой находятся все записи из базы данных.
        """
        with open(cls.filename, "r", encoding="utf-8") as file:
            data = list(map(lambda x: Record(**x), json.load(file)))
        return Phonebook(data)

    @classmethod
    def find_record(cls, find_data: dict) -> Phonebook:
        """Метод для поиска записей.

        Возвращает объект модели Phonebook,
        в которой находятся все записи из базы данных,
        которые соответствуют поисковому запросу пользователя.
        """
        found = []

        with open(cls.filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for record in data:
            for key in find_data:
                if find_data[key] != record[key]:
                    break
            else:
                found.append(Record(**record))

        if found:
            return Phonebook(found)

    @classmethod
    def check_exists_id_in_database(cls, id: int) -> bool:
        """Метод для проверки наличия записи с заданным ID в базе данных."""

        with open(cls.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return len(data) >= id

    @classmethod
    def edit_record(cls, id: int, edit_data: dict) -> None:
        """
        Метод для изменения записи в базе данных,
        которая соответсвует заданному ID.
        """
        with open(cls.filename, "r+", encoding="utf-8") as file:
            data = json.load(file)

            for key in edit_data:
                data[id - 1][key] = edit_data[key]

            file.seek(0)
            json.dump(data, file, indent=4)
