from django.db import models
from manage import init_django
from datetime import (
    datetime,
    time,
    date,
)
from asgiref.sync import sync_to_async
from typing import List

DEBUG = False

school_list = [
    "№10 (уд. Анны Ахматовой, д.18) - школа",
    "детский сад",
    "№10 (ул. Анны Ахматовой, д.18) - школа",
]


def strintdate(date, format: str = "%d.%m.%Y") -> int | None:
    try:
        return int(date.strftime(format))
    except Exception as error:
        return None


init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class User(Model):
    tg_id = models.IntegerField(
        null=False,
        blank=False,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None,
    )
    allow_user = models.BooleanField(
        null=False,
        blank=False,
        default=False,
    )

    @staticmethod
    @sync_to_async
    def is_have_user(tg_id: int, username: str) -> bool:
        if not User.objects.filter(tg_id=tg_id).exists():
            User.objects.create(
                tg_id=tg_id,
                username=username,
            ).save()
            return True
        return False

    @staticmethod
    @sync_to_async
    def is_allow_user(tg_id: int) -> bool:
        return User.objects.get(tg_id=tg_id).allow_user

    @staticmethod
    @sync_to_async
    def set_allow_user(tg_id: int) -> bool:
        try:
            obj = User.objects.get(tg_id=tg_id)
            obj.allow_user = True
            obj.save()
            return True
        except Exception as error:
            print(error)
            return False

    @staticmethod
    @sync_to_async
    def get_all_allow_user_tg_id() -> List[int]:
        return [obj.tg_id for obj in User.objects.filter(allow_user=True)]

    def __str__(self):
        return f"{self.tg_id}:{self.username}:{self.allow_user}"


class LineSheet(Model):
    time_tag = models.TextField(blank=True, verbose_name="Отметка времени")
    school = models.TextField(blank=True, verbose_name="Образовательная площадка")
    teacher = models.TextField(blank=True, verbose_name="Ф.И.О. учителя/воспитателя")
    companion = models.TextField(
        blank=True,
        verbose_name="Сопровождающие (полностью Ф.И.О) ВНИМАНИЕ!!! Сопровождающими могут быть ТОЛЬКО сотрудники комплекса",
    )
    date_departure = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата выезда",
        default=None,
    )
    time_departure = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name="Время выезда",
        default=None,
    )
    date_arrival = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата приезда",
        default=None,
    )
    time_arrival = models.TimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name="Время приезда обратно",
        default=None,
    )
    class_tag = models.TextField(blank=True, verbose_name="Номер и литера класса")
    students_count = models.IntegerField(
        blank=True, verbose_name="Количество обучающихся"
    )
    event = models.TextField(
        blank=True,
        verbose_name="Название мероприятия",
    )
    adress = models.TextField(blank=True, verbose_name="Адрес проведения мероприятия ")
    transport = models.TextField(
        blank=True,
        verbose_name="На каком виде транспорта Вы будете добираться до места проведения мероприятия",
    )
    students = models.TextField(
        blank=True,
        verbose_name="№, Ф.И.О. обучающихся, дата рождения, класс, ФИО и № телефона одного из родителей/законного представителя)",
    )

    def __str__(self) -> str:
        return self.time_tag

    def all(self) -> str:
        result_line = str()
        for key, value in zip(self.__dict__.keys(), self.__dict__.values()):
            if key not in ["_state", "id", "created_at"]:
                result_line += f"{key}:{value}\n"
        return result_line

    @sync_to_async
    def save(self, *args, **kwargs) -> int:
        super(LineSheet, self).save(*args, **kwargs)
        return self.id

    def full_clean(self) -> None:
        self.date_departure = LineSheet.validate_date(str_date=str(self.date_departure))
        self.date_arrival = LineSheet.validate_date(str_date=str(self.date_arrival))
        self.time_departure = LineSheet.validate_time(str_time=str(self.time_departure))
        self.time_arrival = LineSheet.validate_time(str_time=str(self.time_arrival))
        return super().full_clean()

    @staticmethod
    def validate_date(str_date: str) -> date | None:
        """Если можем преобразуем дату к единому формату, если нет записываем NULL"""
        date_format = "%d.%m.%Y"
        try:
            return datetime.strptime(str_date, date_format).date()
        except Exception as error:
            return None

    @staticmethod
    def validate_time(str_time: str) -> time | None:
        """Если можем преобразуем время к текущему формату, если нет записываем NULL"""
        time_format = "%H:%M:%S"
        try:
            return datetime.strptime(str_time, time_format).time()
        except Exception as error:
            return None

    def __eq__(self, other) -> bool:
        """Два объекта равны, если равны их time_tag"""
        if self.time_tag == other.time_tag:
            return True
        return False

    @sync_to_async
    def validate(self) -> bool:
        """Если time_tag последнего и текущего не равны
        и текущая школа валидная"""
        if DEBUG:
            return True
        if not self.not_equal():
            """Если time_tag совпали возвращаем False и не идем проверять школу"""
            return False
        if self.validate_school():
            return True
        return False

    def not_equal(self) -> bool:
        """Если текущая строка равна строке последней записанной строке"""
        if self != LineSheet.objects.last():
            return True
        print(
            f"It is not a new time_tag:\nlast:{LineSheet.objects.last().time_tag}\nnow:{self.time_tag}"
        )
        return False

    @staticmethod
    def find(string: str, find_string: str) -> bool:
        if string.find(find_string) != -1:
            return True
        return False

    def validate_school(self) -> bool:
        """Если в текущей школе есть одно из school_list"""

        find_school_list = [
            LineSheet.find(self.school, find_school) for find_school in school_list
        ]
        if any(find_school_list):
            return True
        print(f"School is not validate:{self.school}")
        return False

    def compare_month(self, month: int) -> bool:
        if strintdate(date=self.date_departure, format="%m") == month:
            return True
        return False

    def print(self) -> None:
        print(self.all())
