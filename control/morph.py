from typing import List
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender


verbs = {
    "именительный": 0,
    "родительный": 1,
    "дательный": 2,
    "винительный": 3,
}


class Morph:
    def __init__(self, line: str, case_form) -> None:
        self._p = Petrovich()
        self._case_id = verbs[case_form]
        self._splited_line = line.split()
        self.cased_list = self.get_cased_list()
        self.word = self.get_word()

    def get_cased_list(self) -> List:
        cased_list = list()
        for index in range(0, len(self._splited_line), 3):
            try:
                cased_list.append(
                    self.get_full_name(
                        [
                            self._splited_line[index + 0],
                            self._splited_line[index + 1],
                            self._splited_line[index + 2],
                        ]
                    )
                )
            except Exception as error:
                pass
        return cased_list

    def get_full_name(self, word):
        try:
            case_lastname = self._p.lastname(word[0], self._case_id)
            case_firstname = self._p.firstname(word[1], self._case_id)
            case_middlename = self._p.middlename(word[2], self._case_id)
            return f"{case_lastname} {case_firstname} {case_middlename}"
        except Exception as error:
            return f"{word[0]} {word[1]} {word[2]}"

    def get_word(self):
        return " ".join(word for word in self.cased_list)
