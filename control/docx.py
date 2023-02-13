import os
from docxtpl import DocxTemplate
from typing import (
    Dict,
    Any,
)


class Docx:
    def __init__(
        self, template_name: str, context: Dict[str, Any], doc_name: str
    ) -> None:
        self._template_name = template_name
        self._context = context
        self._doc_name = doc_name
        self.render()

    def render(self):
        template = DocxTemplate(self._template_name)
        try:
            template.render(self._context)
            template.save(self._doc_name)
        except Exception as ex:
            print(f"Error for render and save template {self._doc_name}")
