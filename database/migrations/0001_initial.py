# Generated by Django 4.1.6 on 2023-05-09 16:07

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LineSheet",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "time_tag",
                    models.TextField(blank=True, verbose_name="Отметка времени"),
                ),
                (
                    "school",
                    models.TextField(
                        blank=True, verbose_name="Образовательная площадка"
                    ),
                ),
                (
                    "teacher",
                    models.TextField(
                        blank=True, verbose_name="Ф.И.О. учителя/воспитателя"
                    ),
                ),
                (
                    "companion",
                    models.TextField(
                        blank=True,
                        verbose_name="Сопровождающие (полностью Ф.И.О) ВНИМАНИЕ!!! Сопровождающими могут быть ТОЛЬКО сотрудники комплекса",
                    ),
                ),
                (
                    "date_departure",
                    models.DateField(
                        blank=True, default=None, null=True, verbose_name="Дата выезда"
                    ),
                ),
                (
                    "time_departure",
                    models.TimeField(
                        blank=True, default=None, null=True, verbose_name="Время выезда"
                    ),
                ),
                (
                    "date_arrival",
                    models.DateField(
                        blank=True, default=None, null=True, verbose_name="Дата приезда"
                    ),
                ),
                (
                    "time_arrival",
                    models.TimeField(
                        blank=True,
                        default=None,
                        null=True,
                        verbose_name="Время приезда обратно",
                    ),
                ),
                (
                    "class_tag",
                    models.TextField(blank=True, verbose_name="Номер и литера класса"),
                ),
                (
                    "students_count",
                    models.IntegerField(
                        blank=True, verbose_name="Количество обучающихся"
                    ),
                ),
                (
                    "event",
                    models.TextField(blank=True, verbose_name="Название мероприятия"),
                ),
                (
                    "adress",
                    models.TextField(
                        blank=True, verbose_name="Адрес проведения мероприятия "
                    ),
                ),
                (
                    "transport",
                    models.TextField(
                        blank=True,
                        verbose_name="На каком виде транспорта Вы будете добираться до места проведения мероприятия",
                    ),
                ),
                (
                    "students",
                    models.TextField(
                        blank=True,
                        verbose_name="№, Ф.И.О. обучающихся, дата рождения, класс, ФИО и № телефона одного из родителей/законного представителя)",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("tg_id", models.IntegerField(unique=True)),
                (
                    "username",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("allow_user", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
