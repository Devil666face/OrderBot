from database.models import LineSheet

exam_tag = [
    "ЕГЭ",
    "ОГЭ",
    "основной государственный экзамен",
    "основного государственного экзамена",
    "экзамен",
    "экзамена",
]


class Control:
    def __init__(self, last_line: LineSheet) -> None:
        self.last_line = last_line
        self.template_name = self.get_template_name()
        print(self.template_name)

    def get_template_name(self):
        if self.is_exam():
            return "template/exam_template.docx"
        elif self.is_school():
            return "template/event_template.docx"
        else:
            return "template/other_template.docx"

    def is_exam(self) -> bool:
        for tag in exam_tag:
            if LineSheet.find(
                string=self.last_line.event.lower(), find_string=tag.lower()
            ):
                return True
        return False

    def is_school(self) -> bool:
        if LineSheet.find(string=self.last_line.school.lower(), find_string="школа"):
            return True
        return False
