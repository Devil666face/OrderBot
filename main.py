from api.googlesheet import GoogleSheet


def main():
    sheet = GoogleSheet()
    # values = sheet.get_for_number(line_number=1792)
    last_line = sheet.last
    last_line.full_clean()
    # last_line.save()
    validation = last_line.validate()
    print(validation)


if __name__ == "__main__":
    main()
