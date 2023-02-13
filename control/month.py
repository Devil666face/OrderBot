import os
import xlsxwriter
from fuzzywuzzy import fuzz
from typing import List
from database.models import LineSheet
from collections import Counter
from control.parser import (
    Parser,
    strftime,
    strfdate,
)


class MonthReport:
    def __init__(self, month_number: int, values_for_month: List[LineSheet]) -> None:
        self.month_number = month_number
        self.values_for_month: List[LineSheet] = values_for_month
        self.list_for_record_none_check = self.make_data_for_table()
        self.classroom_teachers = self.get_classroom_teachers()
        self.data_for_record = self.check_classroom_teachers(
            values_for_record=self.list_for_record_none_check,
            classroom_teachers=self.classroom_teachers,
        )
        self.file_name = self.write()

    def get_classroom_teachers(self):
        classroom_teachers = list()
        for line in self.values_for_month:
            try:
                if line.time_tag not in ["", "класс"]:
                    classroom_teachers.append([line.time_tag, line.school])
            except Exception as error:
                pass
        return classroom_teachers

    def get_month_name(self, month_number: int) -> str:
        month = {
            1: "январь",
            2: "февраль",
            3: "март",
            4: "апрель",
            5: "май",
            6: "июнь",
            7: "июль",
            8: "август",
            9: "сентябрь",
            10: "октябрь",
            11: "ноябрь",
            12: "декабрь",
        }
        return month.get(month_number, str(month_number))

    def write(self) -> str:
        file_name = f"{self.get_month_name(self.month_number)}.xlsx"
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet(
            name=f"{self.get_month_name(self.month_number)}"
        )
        for i, line in enumerate(self.data_for_record):
            for j, cell in enumerate(line):
                worksheet.write(i, j, cell)
        workbook.close()
        return file_name

    def make_data_for_table(self):
        list_for_record_none_check = list()
        for line in self.values_for_month:
            parser = Parser(data=line)
            class_counter, class_count = self.get_class(
                parser.make_student_list(line.students)
            )
            list_for_record_none_check.append(
                [
                    line.teacher,
                    "нет",
                    strfdate(line.date_arrival),
                    strftime(line.time_arrival),
                    class_counter,
                    class_count,
                ]
            )
        return list_for_record_none_check

    def check_classroom_teachers(self, values_for_record, classroom_teachers):
        def s(value):
            return str(value).strip()

        for index, line in enumerate(values_for_record):
            teacher_list = line[0]
            class_label = line[4]
            for teacher in teacher_list.split(","):
                for classroom_line in classroom_teachers:
                    true_class_label = classroom_line[0]
                    true_class_teacher = classroom_line[1]
                    print((teacher), s(true_class_teacher))
                    if s(teacher) == s(true_class_teacher):
                        # Использую нечеткое сравнение. Порог истины 80%
                        print(s(class_label), s(true_class_label))
                        if fuzz.ratio(s(class_label), s(true_class_label)) >= 80:
                            values_for_record[index][1] = "да"
                            break
                break
        return values_for_record

    def get_class(self, class_list):
        def get_most_common(lable_list):
            try:
                return Counter(class_label).most_common(1)[0][0]
            except Exception as ex:
                return "-"

        class_label = list()
        for line in class_list:
            pupil = line.get("cols", None)
            if pupil is not None:
                class_label.append(str(pupil[2]).replace("обучающийся ", "").upper())
        return get_most_common(class_label), len(class_list)
