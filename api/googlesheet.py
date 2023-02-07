import os.path

# import datetime
# from datetime import datetime
from dataclasses import dataclass
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database.models import LineSheet

DEBUG_MODE = False


class GoogleSheet:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    SAMPLE_SPREADSHEET_ID = "18czznNPJKfFsAFNrAgL_Nvxgc_Lea4-ghwMNaHt-3aM"
    SAMPLE_RANGE_NAME = "Ответы на форму (1)"

    def __init__(self):
        if os.path.exists("creeds/token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "creeds/token.json", self.SCOPES
            )
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "creeds/credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=8080)
            with open("creeds/token.json", "w") as token:
                token.write(self.creds.to_json())

        try:
            service = build("sheets", "v4", credentials=self.creds)
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(
                    spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                    range=self.SAMPLE_RANGE_NAME,
                )
                .execute()
            )
            self._values = result.get("values", [])[1:]
            if self._values:
                self.last = self.make_typing_from_line(line=self._values[-1])

        except HttpError as err:
            print(err)

    def get_for_number(self, line_number: int) -> list[list[str]]:
        """Возвращает строку из таблицы по табличному номеру,
        если такой строки нет возвращает последнюю строку,
        если данные из таблицы не получены вызывает ошибку"""
        if self._values:
            try:
                return self.make_typing_from_line(line=self._values[line_number - 2])
            except IndexError as error:
                print(error, f"No data for number {line_number}")
            return self.make_typing_from_line(line=self._values[-1])
        raise ValueError("I have no data from Google Sheet")

    def make_typing_from_line(self, line: list[str]) -> LineSheet:
        line[8] = "qwdqwd"
        line_typing = LineSheet(
            time_tag=line[0],
            school=line[2],
            teacher=line[3],
            event=line[4],
            date_departure=line[5],
            time_departure=line[6],
            date_arrival=line[7],
            time_arrival=line[8],
            transport=line[9],
            adress=line[10],
            route=line[11],
            students=line[12],
            companion=line[13],
            plan=line[14],
            email=line[15],
            number=line[16],
        )
        return line_typing


#     def get_values_from_sheet(self, last_twenty: bool, current_index=-1):
#         if not self.values:
#             return False

#         if current_index != -1:
#             return self.values[current_index]

#         if last_twenty:
#             return self.values[len(self.values) - 20 : len(self.values)], len(
#                 self.values
#             )

#         last_line_index, last_date_value = self.find_last_date_line()
#         print(last_line_index, last_date_value, self.database.get_last_record())

#         if self.database.get_last_record() != last_date_value or DEBUG_MODE:
#             self.database.update_last_record(last_date_value)
#             return self.create_doc(last_line_index)
#         else:
#             print(f"Its not new record {last_date_value}")
#             return False

#     def create_doc(self, last_line_index):
#         last_line = self.values[last_line_index]
#         if self.organization_check(last_line[2]):
#             return last_line
#         else:
#             return False

#     def find_last_date_line(self):
#         # for date_value in self.values:
#         print(self.values)
#         date_dict = {
#             index: date_value[0] for index, date_value in enumerate(self.values)
#         }
#         # print(self.date_dict)
#         ordered_data = sorted(
#             date_dict.items(),
#             key=lambda x: datetime.strptime(x[1], "%d.%m.%Y %H:%M:%S"),
#             reverse=True,
#         )
#         # print(ordered_data)
#         # print(ordered_data[0][0],ordered_data[0][1])
#         return ordered_data[0][0], ordered_data[0][1]

#     def organization_check(self, value):
#         if DEBUG_MODE:
#             return True
#         if str(value).find("№10 (уд. Анны Ахматовой, д.18) - школа") != -1:
#             return True
#         if str(value).find("детский сад") != -1:
#             return True
#         return False


# def make_document():
#     API = SheetAPI(Database())
#     last_line = API.get_values_from_sheet(last_twenty=False)
#     if not last_line:
#         return False
#     replacer = DocumentController(last_line)
#     doc_name = replacer.generate_document()
#     return doc_name


# def make_document_for_line(last_line):
#     replacer = DocumentController(last_line)
#     doc_name = replacer.generate_document()
#     return doc_name


# def get_last_twenty():
#     API = SheetAPI(Database())
#     last_twenty_line, max_len = API.get_values_from_sheet(last_twenty=True)
#     return last_twenty_line, max_len


# def get_for_current_line(current_index):
#     API = SheetAPI(Database())
#     return API.get_values_from_sheet(last_twenty=False, current_index=current_index)
