from api.googlesheet import GoogleSheet
from database.models import LineSheet
from control.control import Control
from control.parser import Parser
from control.docx import Docx
from control.month import MonthReport


def render(last_line: LineSheet):
    parser = Parser(data=last_line)
    Docx(
        template_name=Control(last_line=last_line).template_name,
        context=parser.context,
        doc_name=parser.doc_name,
    )
    return parser.doc_name


async def last():
    sheet = GoogleSheet()
    last_line = sheet.last
    last_line.full_clean()
    validation = await last_line.validate()
    if not validation:
        return
    await last_line.save()
    return render(last_line)


async def month(month_number: int):
    sheet = GoogleSheet()
    all_values = sheet.typing_all()
    line_list_for_order = list()
    for line in all_values:
        line.full_clean()
        if not line.compare_month(month=month_number):
            continue
        if not line.validate_school():
            continue
        line_list_for_order.append(line)
    file_name = MonthReport(month_number, line_list_for_order).file_name
    return file_name


def for_number(number: int) -> str:
    sheet = GoogleSheet()
    last_line = sheet.get_for_number(line_number=number)
    last_line.full_clean()
    return render(last_line)
