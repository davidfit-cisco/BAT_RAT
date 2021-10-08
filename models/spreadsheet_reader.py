import csv
from io import StringIO


class SpreadsheetReader:
    def __init__(self, filename, file_contents):
        self.filename = filename
        self.file_contents = file_contents
        self.column_indexes = {}

        # Initial setup functions
        self._rows = list(csv.reader(StringIO(self.file_contents)))
        self.init_column_indexes()

    @property
    def rows(self):
        return self._rows

    def init_column_indexes(self):
        for index, title in enumerate(list(self._rows)[0]):
            self.column_indexes[title] = index

    def get_cell(self, row, column_name):
        try:
            return row[self.column_indexes[column_name]]
        except KeyError:
            raise KeyError(f"Column with exact name '{column_name}' not found in {self.filename}")

