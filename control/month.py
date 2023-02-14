import xlsxwriter
from dataclasses import dataclass
from fuzzywuzzy import fuzz
from typing import (
    List,
    Dict,
    Literal,
    Tuple,
)
from database.models import LineSheet
from collections import Counter
from control.parser import (
    Parser,
    strftime,
    strfdate,
)


@dataclass
class RecordLine:
    teacher: str
    is_class_teacher: bool
    date_arrival: str
    time_arrival: str
    class_label: str
    class_count: int


class MonthReport:
    def __init__(
        self,
        month_number: int,
        values_for_month: List[LineSheet],
        teacher_list: List[str],
    ) -> None:
        self.month = MonthReport.get_month_name(month_number)
        self.teacher_list = teacher_list
        self.values_for_month: List[LineSheet] = values_for_month
        self.list_for_record_none_check: List[RecordLine] = self.make_data_for_table()
        self.file_name = self.write(data_for_record=self.list_for_record_none_check)

    @staticmethod
    def get_month_name(month_number: int) -> str:
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

    def make_data_for_table(self) -> List[RecordLine]:
        list_for_record_none_check: List[RecordLine] = list()
        for line in self.values_for_month:
            parser = Parser(data=line)
            class_label, class_count = self.get_class(
                parser.make_student_list(line.students)
            )
            list_for_record_none_check.append(
                RecordLine(
                    teacher=line.teacher,
                    is_class_teacher=False,
                    date_arrival=strfdate(line.date_arrival),
                    time_arrival=strftime(line.time_arrival),
                    class_label=class_label,
                    class_count=class_count,
                )
            )
        return list_for_record_none_check

    def write(self, data_for_record: List[RecordLine]) -> str:
        def convert_for_write(line: RecordLine) -> Tuple[str]:
            is_class_teacher = "да" if line.is_class_teacher else "нет"
            return (
                line.teacher,
                is_class_teacher,
                line.date_arrival,
                line.time_arrival,
                line.class_label,
                line.class_count,
            )

        file_name = f"{self.month}.xlsx"
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet(name=self.month)
        for i, line in enumerate(data_for_record):
            for j, cell in enumerate(convert_for_write(line)):
                worksheet.write(i, j, cell)
        workbook.close()
        return file_name

    def get_class(
        self, class_list: List[Dict[Literal["cols"], List]]
    ) -> Tuple[str, int]:
        def get_most_commot_class_label(class_label_list: List[str]) -> str:
            try:
                return Counter(class_label_list).most_common(1)[0][0]
            except Exception as error:
                return "-"

        class_label_list = list()
        for line in class_list:
            pupil_list = line.get("cols", None)
            if pupil_list is None:
                continue
            class_label = str(pupil_list[2]).replace("обучающийся ", "").upper()
            class_label_list.append(class_label)
        return get_most_commot_class_label(class_label_list), len(class_label_list)
