from api.googlesheet import GoogleSheet


def last():
    sheet = GoogleSheet()
    last_line = sheet.last
    last_line.full_clean()
    validation = last_line.validate()
    if not validation:
        return
    last_line.save()
    print(validation)
    last_line.print()


def for_number(number: int):
    sheet = GoogleSheet()
    last_line = sheet.get_for_number(line_number=1781)
    last_line = sheet.last
    last_line.full_clean()
    last_line.print()


if __name__ == "__main__":
    last()
