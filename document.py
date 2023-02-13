from api.googlesheet import GoogleSheet
from database.models import LineSheet
from control.control import Control
from control.parser import Parser
from control.docx import Docx


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
    validation = last_line.validate()
    if not validation:
        return
    await last_line.save()
    return render(last_line)


def for_number(number: int) -> str:
    sheet = GoogleSheet()
    last_line = sheet.get_for_number(line_number=number)
    last_line.full_clean()
    return render(last_line)
