import os.path
from typing import List
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from database.models import LineSheet


class GoogleSheet:
    def __init__(
        self,
        path_to_token: str = "creeds/token.json",
        SCOPES: List[str] = ["https://www.googleapis.com/auth/spreadsheets.readonly"],
        SAMPLE_SPREADSHEET_ID: str = "18czznNPJKfFsAFNrAgL_Nvxgc_Lea4-ghwMNaHt-3aM",
        SAMPLE_RANGE_NAME: str = "Ответы на форму (1)",
    ):
        if os.path.exists(path_to_token):
            self.creds = Credentials.from_authorized_user_file(path_to_token, SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "creeds/credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=8080)
            with open(path_to_token, "w") as token:
                token.write(self.creds.to_json())

        try:
            service = build("sheets", "v4", credentials=self.creds)
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=SAMPLE_RANGE_NAME,
                )
                .execute()
            )
            self._values = result.get("values", [])[1:]
            if self._values and path_to_token:
                self.last = self.make_typing_from_line(line=self._values[-1])

        except HttpError as err:
            print(err)

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
            self.last = self.make_typing_from_line(line=self._values[-1])
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
