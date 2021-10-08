from copy import deepcopy
from models.spreadsheet_reader import SpreadsheetReader
from utils.utils import is_date, add_date_to_data, is_open_dg_store, is_registered, is_unregistered, \
    get_file_contents, is_specified_store


class RegistrationAnalysisTool:
    """
    The stored file is passed in and the file_contents are retrieved. The SpreadsheetReader class opens the
    spreadsheet and provides some useful methods for traversing the spreadsheet.

    The store_name variable will default to Dollar General unless something else is passed in via the html form on
    rat.html
    """
    def __init__(self, stored_file, store_name="Dollar General"):
        self.main_data = {}
        self.tcp_data = {}
        self.tcp_never_macs = {}
        self.days = []

        self.stored_file = stored_file
        self.store_name = store_name
        self.filename = self.stored_file.filename
        self.filetype = self.filename.split(".")[-1]
        self.file_contents = get_file_contents(self.filetype, self.stored_file)
        self.spreadsheet = SpreadsheetReader(self.filename, self.file_contents)
        self.column_indexes = self.process_title_row()

    def get_data(self):
        self.days = list(self.main_data.keys())
        self.tcp_data = deepcopy(self.main_data)

        for row in self.spreadsheet.rows[1:]:
            if self.store_name.lower() == "all":
                self.process_row(row)
            elif self.store_name.lower() == "dollar general":
                if is_open_dg_store(self.column_indexes, row):
                    self.process_row(row)
            elif is_specified_store(self.column_indexes, row, self.store_name):
                self.process_row(row)

        return self.main_data, self.tcp_data, self.tcp_never_macs, self.days

    def process_row(self, row):
        """
        This method is called on each row in the spreadsheet
        """
        device_type = row[self.column_indexes["device type"]]
        for day in self.days:
            self.initialise_day_data(day, device_type, row)
            self.process_day_data(day, device_type, row)

    def process_day_data(self, day, device_type, row):
        is_tcp = self.is_tcp_store(row)
        reg_count = 0
        unregistered_count = 0
        data = self.main_data
        if is_tcp:
            data = self.tcp_data
        column_count = len(data[day]["columns"])
        for column_index in data[day]["columns"]:
            cell = row[column_index]
            if is_registered(cell):
                reg_count += 1
            if is_unregistered(cell):
                unregistered_count += 1
        if reg_count == column_count:
            data[day]['Always'][device_type] += 1
        elif unregistered_count == column_count:
            data[day]['Never'][device_type] += 1
            if is_tcp and "SPA" in device_type.upper():
                self.tcp_never_macs[day].append(row[self.column_indexes["mac"]])
        else:
            data[day]['Sometimes'][device_type] += 1

    def initialise_day_data(self, day, device_type, row):
        is_tcp = self.is_tcp_store(row)
        data = self.main_data
        if is_tcp:
            data = self.tcp_data
        if device_type not in data[day]['Always']:
            for option in ('Always', 'Sometimes', 'Never'):
                data[day][option][device_type] = 0
        if is_tcp and day not in self.tcp_never_macs:
            self.tcp_never_macs[day] = []

    def process_title_row(self):
        title_row = self.spreadsheet.rows[0]
        column_indexes = {}
        for index, column_name in enumerate(title_row):
            if column_name.lower() == "sitename":
                column_indexes["name1"] = index
            elif column_name.lower() == "customer":
                column_indexes["name2"] = index
            else:
                column_indexes[column_name.lower()] = index
            if is_date(column_name):
                add_date_to_data(index, column_name, self.main_data)
        return column_indexes

    def is_tcp_store(self, row):
        if "tcp?" in self.column_indexes:
            return "tcp" in row[self.column_indexes["tcp?"]].lower()
        return False
