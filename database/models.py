# from django.core.validators import validate_email
from django.db import models

from typing import Any, Literal
from manage import init_django
from datetime import (
    datetime,
    time,
    date,
)

blank = ""

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
        blank=True, null=True, verbose_name="Дата выезда", default=None
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
        blank=True, null=True, verbose_name="Дата приезда", default=None
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
    email = models.EmailField(
        max_length=254, blank=True, verbose_name="Адрес электронной почты"
    )
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

    def validate(self) -> None:
        self.date_departure = LineSheet.validate_date(str_date=self.date_departure)
        self.date_arrival = LineSheet.validate_date(str_date=self.date_arrival)
        self.time_departure = LineSheet.validate_time(str_time=self.time_departure)
        self.time_arrival = LineSheet.validate_time(str_time=self.time_arrival)
        return super().full_clean()

    @staticmethod
    def validate_date(str_date: str | Any) -> date | None:
        date_format = "%d.%m.%Y"
        try:
            return datetime.strptime(str_date, date_format).date()
        except Exception as error:
            return None

    @staticmethod
    def validate_time(str_time: str | Any) -> time | None:
        time_format = "%H:%M:%S"
        try:
            return datetime.strptime(str_time, time_format).time()
        except Exception as error:
            return None
