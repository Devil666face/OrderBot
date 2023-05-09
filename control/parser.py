import re
from typing import (
    List,
    Dict,
    Any,
    Literal,
)
from datetime import datetime
from collections import Counter
from control.morph import Morph
from database.models import (
    LineSheet,
    DEBUG,
)


event_replace_word_list = [
    "О посещении",
    "посещение",
    "Посещение",
]
main_metodier = "Ю.В. Беловой"
second_metodier = "Н.Н. Рыбаковой"
weekend_line = "выход на работу в выходной день"
work_line = "командировку"


def strfdate(date, format: str = "%d.%m.%Y") -> str | None:
    try:
        return date.strftime(format)
    except Exception as error:
        return None


def strftime(time) -> str | None:
    try:
        return time.strftime("%H:%M")
    except Exception as error:
        return None


def get_weekend(date) -> bool:
    try:
        match date.strftime("%A"):
            case "Sunday" | "Saturday":
                return True
            case _:
                return False
    except AttributeError as error:
        return False


class Parser:
    def __init__(self, data: LineSheet) -> None:
        self.data = data
        self.doc_name = self.get_doc_name()
        self.get_variabels()
        self.context = self.get_context()
        if DEBUG:
            print(self.context)

    def get_variabels(self):
        self.main_teacher = self.get_main_teacher(teacher=self.data.teacher)
        self.teacher_list = self.make_teacher_list(
            self.main_teacher, self.data.companion
        )
        self.student_list = self.make_student_list(self.data.students)
        self.second_teacher = self.get_second_teacher()
        self.metodier = self.get_metoditier()
        self.sample_teacher_list = self.get_teacher_list()
        self.type_of_work = self.get_type_of_work()
        self.tutor = self.get_tutor()

    def get_context(self) -> Dict[str, Any]:
        teacher_list_genetive_case = Morph(self.sample_teacher_list, "родительный").word
        return {
            "place": self.get_event(),
            "date": strfdate(self.data.date_departure),
            "where": self.data.adress,
            "starttime": strftime(self.data.time_departure),
            "finishdate": strfdate(self.data.date_arrival),
            "finishtime": strftime(self.data.time_arrival),
            "tbl_contents": [*self.teacher_list, *self.student_list],
            "mainteacher": Morph(self.main_teacher, "дательный").word,
            "secondteacher": Morph(self.second_teacher, "дательный").word,
            "metoditer": self.metodier,
            "tutor": self.tutor,
            "teacherlist_lessons": teacher_list_genetive_case,
            "teacherlist_visit": teacher_list_genetive_case,
            "teacherlist_pay": teacher_list_genetive_case,
            "teacherlist": self.sample_teacher_list,
            "typework": self.type_of_work,
            "paytypework": self.type_of_work.replace("выход на ", ""),
        }

    def get_main_teacher(self, teacher: str) -> str:
        word_list = teacher.strip().split()
        return " ".join(word_list[0:3])

    def get_doc_name(self):
        return f"ОргПриказ - {self.data.teacher.split()[0]} {strfdate(self.data.date_departure)}.docx"

    def get_event(self) -> str:
        event = self.data.event
        for word in event_replace_word_list:
            if event.find(word) != -1:
                return event.replace(word, "").strip()
        return event.strip()

    def get_teacher_list(self) -> str:
        return ", ".join(
            str(teacher["cols"][1]).strip() for teacher in self.teacher_list
        )

    def get_metoditier(self) -> str:
        number_list = []
        for classmate in self.student_list:
            s: List[int] = list()
            for number in re.findall(r"-?\d+\.?\d*", classmate["cols"][2]):
                try:
                    s.append(int(number))
                except:
                    pass
            try:
                number_list.append(s[0])
            except:
                pass
        try:
            if int(Counter(number_list).most_common(1)[0][0]) <= 4:
                return second_metodier
            else:
                return main_metodier
        except:
            return main_metodier

    def get_second_teacher(self):
        if len(self.teacher_list) == 1:
            return self.teacher_list[0]["cols"][1]
        return self.teacher_list[1]["cols"][1]

    def make_teacher_list(self, mainteacher_line: str, otherteacher_line: str):
        def make_main_teacher(mainteacher_line: str) -> List[Dict[str, str]]:
            teacher_dict = {}
            teacher_dict["cols"] = ["", mainteacher_line, "учитель"]
            return [teacher_dict]

        def make_other_teacher(
            mainteacher_line: str, otherteacher_line: str
        ) -> List[Dict[str, str]]:
            other_teacher_list = []
            splited_otherteacher_line = []
            for word in re.findall(r"\w+", otherteacher_line):
                if not word.isnumeric():
                    splited_otherteacher_line.append(word)
            for index in range(0, len(splited_otherteacher_line), 4):
                try:
                    teacher_name = f"{splited_otherteacher_line[index]} {splited_otherteacher_line[index+1]} {splited_otherteacher_line[index+2]}"
                    other_teacher_dict = {}
                    if mainteacher_line.strip() != teacher_name.strip():
                        other_teacher_dict["cols"] = ["", teacher_name, "учитель"]
                        other_teacher_list.append(other_teacher_dict)
                except Exception as error:
                    pass
            return other_teacher_list

        return [
            *make_main_teacher(mainteacher_line),
            *make_other_teacher(mainteacher_line, otherteacher_line),
        ]

    def make_student_list(
        self, data_in_one_cell: str
    ) -> List[Dict[Literal["cols"], List]]:
        def get_student_name(student_line: str) -> str:
            splited_line = re.split(r"\d+", student_line, maxsplit=1)[1]
            without_first_dot = re.split(r".", splited_line, maxsplit=1)[1]
            return str(without_first_dot).strip()

        def get_student_classmate(student_line: str) -> str:
            line = student_line.split(",")[2]
            return str(line).strip()

        student_list = list()
        number = 1
        for line in data_in_one_cell.split("\n"):
            try:
                if len(line) == 0:
                    raise Exception
                name = get_student_name(line)
                if not name:
                    raise Exception
                classmate = get_student_classmate(line)
                line_dict = {}
                line_dict["cols"] = [f"{number}", name, f"обучающийся {classmate}"]
                student_list.append(line_dict)
                number += 1
            except Exception as ex:
                pass
        return student_list

    def get_type_of_work(self) -> str:
        if get_weekend(self.data.date_departure):
            return weekend_line
        return work_line

    def get_tutor(self) -> str:
        match self.data.school:
            case "№ 3 (ул. Анны Ахматовой, д.2, корп.1) - детский сад":
                return "Р.П.Мудункаевой"
            case "№ 9 (ул. Бориса Пастернака д.27а) - детский сад" | "№ 2 (ул. Летчика Грицевца, д.5, корп.1) - детский сад" | "№ 6 (ул. Летчика Ленина, 2А) - детский сад»":
                return "Н.А. Филимоновой"
            case "№ 15 (ул. Бориса Пастернака д.47а) - детский сад" | "№ 16 (ул. Бориса Пастернака д.8а) - детский сад":
                return "Т.Н. Фортуновой"
            case "№ 11 (ул. Анны Ахматовой, д.16а) - детский сад" | "№ 12 (ул. Анны Ахматовой, д.20) - детский сад":
                return "Л.Х. Мамедовой"
            case _:
                return "Имя воспитателя"
