from math import ceil

LIMIT_OF_RECORDS_ON_ONE_PAGE = 5


class Record:
    """Модель для записи.

    Содержит в себе ID, фамилию, имя, отчество,
    название организации, рабочий и личный номера телефонов.
    """

    def __init__(
        self,
        id: int,
        surname: str,
        name: str,
        patronymic: str,
        organization_name: str,
        work_phone: str,
        personal_phone: str,
    ) -> None:
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.organization_name = organization_name
        self.work_phone = work_phone
        self.personal_phone = personal_phone
        self.validate()

    def validate(self) -> None:
        """Метод валидации создания новой записи.

        Проверяет, что все атрибуты были переданы,
        в противном случае выбрасывает исключение.
        """
        for value in self.__dict__.values():
            if not value:
                raise ValueError(
                    "Невозможно создать запись, "
                    "все поля должны быть заполнены."
                )


class Phonebook:
    """Модель для телефонного справочника.

    Содержит в себе номер страницы и список всех записей,
    которые являются объектами модели Record.
    """

    page: int = 1

    def __init__(self, records: list[Record]) -> None:
        self.records = records

    def show_page(self) -> list[Record]:
        """Метод для показа актуальной страницы.

        Возвращает список записей актуальной страницы справочника.
        """
        return self.records[
            LIMIT_OF_RECORDS_ON_ONE_PAGE
            * (self.page - 1): LIMIT_OF_RECORDS_ON_ONE_PAGE
            * self.page
        ]

    def next_page(self) -> None:
        """Метод для перехода на следующую страницу справочника."""
        self.page += 1

    def back_page(self) -> None:
        """Метод для перехода на предыдущую страницу справочника."""
        self.page -= 1

    def possible_commands(self) -> str:
        """Метод для получения валидных команд при просмотре страницы.

        С помощью количества записей и лимита записей на одну страницу,
        возвращает список команд,
        которые не противоречат наполненности базы данных.
        """

        if (
            self.page >= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE)
            and self.page == 1
        ):
            return "\n".join(["0. В главное меню"])
        if (
            self.page >= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE)
            and self.page > 1
        ):
            return "\n".join(["2. Предыдущая страница", "0. В главное меню"])
        if (
            self.page <= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE)
            and self.page == 1
        ):
            return "\n".join(["1. Следующая страница", "0. В главное меню"])
        if (
            self.page <= ceil(len(self.records) / LIMIT_OF_RECORDS_ON_ONE_PAGE)
            and self.page > 1
        ):
            return "\n".join(
                [
                    "1. Следующая страница",
                    "2. Предыдущая страница",
                    "0. В главное меню",
                ]
            )


class Table:
    """Модель для таблицы вывода записей.

    Принимает названия столбцов (заголовок) и объект модели справочника.
    """

    def __init__(self, header: list[str], phonebook: Phonebook) -> None:
        self.header = header
        self.phonebook = phonebook
        self.page_of_records = phonebook.show_page()
        max_length_header = max([len(column) for column in header])
        max_length_record = max(
            [
                max(list(map(lambda x: len(str(x)), record.__dict__.values())))
                for record in self.page_of_records
            ]
        )
        self.max_len = max(max_length_header, max_length_record) + 3

    def show_table(self) -> str:
        """Метод для показа таблицы.

        Возвращает готовую таблицу с заголовком,
        разделительными линиями и записями.
        """
        header = "|".join(
            [word.center(self.max_len, " ") for word in self.header]
        )
        string_of_page_number = (
            f" Страница {str(self.phonebook.page)} ".center(len(header), "-")
        )
        demarcation_line = "-" * len(header)
        records = [
            "|".join(
                [
                    str(word).center(self.max_len, " ")
                    for word in record.__dict__.values()
                ]
            )
            for record in self.page_of_records
        ]
        return "\n".join(
            [
                string_of_page_number,
                header,
                demarcation_line,
                *records,
                demarcation_line,
            ]
        )
