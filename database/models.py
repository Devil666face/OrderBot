# from django.core.validators import validate_email
from django.db import models

from typing import Any, Literal
from manage import init_django
from datetime import (
    datetime,
    time,
    date,
)

DEBUG = False
school_list = [
    "№10 (уд. Анны Ахматовой, д.18) - школа",
    "детский сад",
    "№10 (ул. Анны Ахматовой, д.18) - школа",
]


init_django()


class Model(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class LineSheet(Model):
    time_tag = models.TextField(blank=True, verbose_name="Отметка времени")
    school = models.TextField(blank=True, verbose_name="Образовательная площадка")
    teacher = models.TextField(
        blank=True, verbose_name="Ф.И.О. учителя/воспитателя (ПОЛНОСТЬЮ) *"
    )
    event = models.TextField(
        blank=True,
        verbose_name="Название мероприятия (в родительном падеже).  О посещении ....",
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
    transport = models.TextField(
        blank=True,
        verbose_name="На каком виде транспорта Вы будете добираться до места проведения мероприятия",
    )
    adress = models.TextField(blank=True, verbose_name="Адрес проведения мероприятия ")
    route = models.TextField(
        blank=True,
        verbose_name="Опишите маршрут движения (как и на чем будете добираться до места)",
    )
    students = models.TextField(
        blank=True,
        verbose_name="№, Ф.И.О. обучающихся, дата рождения, класс, ФИО и № телефона одного из родителей/законного представителя)",
    )
    companion = models.TextField(
        blank=True,
        verbose_name="Сопровождающие (полностью Ф.И.О) ВНИМАНИЕ!!! Сопровождающими могут быть ТОЛЬКО сотрудники комплекса",
    )
    plan = models.TextField(
        blank=True, verbose_name="Укажите план мероприятия (согласно пунктам)"
    )
    email = models.TextField(blank=True, verbose_name="Адрес электронной почты")
    number = models.TextField(blank=True, verbose_name="Номер телефона для контакта")

    def __str__(self) -> str:
        return self.time_tag

    def all(self) -> str:
        result_line = str()
        for key, value in zip(self.__dict__.keys(), self.__dict__.values()):
            if key not in ["_state", "id", "created_at"]:
                result_line += f"{key}:{value}\n"
        return result_line

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

    def print(self) -> None:
        print(self.all())
