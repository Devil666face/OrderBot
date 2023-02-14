import os.path
from datetime import datetime
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database.models import LineSheet


def strptime_date_tag(date_tag: str) -> datetime:
    return datetime.strptime(date_tag, "%d.%m.%Y %H:%M:%S")


class GoogleSheet:
    def __init__(
        self,
        token="creds/token.json",
        SCOPES=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        SAMPLE_SPREADSHEET_ID="18czznNPJKfFsAFNrAgL_Nvxgc_Lea4-ghwMNaHt-3aM",
        SAMPLE_RANGE_NAME="Ответы на форму (1)",
    ):
        self.token = token
        self.creds = None
        self.SCOPES = SCOPES
        self.SAMPLE_SPREADSHEET_ID = SAMPLE_SPREADSHEET_ID
        self.SAMPLE_RANGE_NAME = SAMPLE_RANGE_NAME
        if os.path.exists(token):
            self.creds = Credentials.from_authorized_user_file(token, self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "creds/credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=8080)
            with open(token, "w") as token:
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
            # if self._values:
            #     self.last = self.make_typing_from_line(line=self._values[-1])

        except HttpError as err:
            print(err)

    def last(self):
        date_tag_dict = dict()
        date_list = list()
        for index, value in enumerate(self._values):
            date_tag = strptime_date_tag(value[0])
            date_tag_dict[date_tag] = index
            date_list.append(date_tag)
        date_list.sort(key=lambda x: x, reverse=False)
        last = date_list[-1]
        index_of_last = date_tag_dict[last]
        return self.make_typing_from_line(line=self._values[index_of_last])

    def get_for_number(self, line_number: int) -> LineSheet:
        """Возвращает строку из таблицы по табличному номеру,
        если такой строки нет возвращает последнюю строку,
        если данные из таблицы не получены вызывает ошибку"""
        if self._values:
            try:
                self.last = self.make_typing_from_line(
                    line=self._values[line_number - 2]
                )
                return self.last
            except IndexError as error:
                print(error, f"No data for number {line_number}")
            self.last = self.last()
            return self.last
        raise ValueError("I have no data from Google Sheet")

    def typing_all(self) -> List[LineSheet]:
        all_typing_list = list()
        for line in self._values:
            all_typing_list.append(self.make_typing_from_line(line=line))
        return all_typing_list

    def make_typing_from_line(self, line: list[str]) -> LineSheet:
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
