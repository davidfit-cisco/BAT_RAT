import os
import chardet
import openpyxl
import pandas as pd
import re
from calendar import month_name
from copy import deepcopy

ALLOWED_EXTENSIONS = ('csv', 'xls', 'xlsx')
SHORT_MONTH_NAMES = [month[:3] for month in month_name[1:]]


def is_mpp(bems_product):
    return "MPP" in bems_product or "DECT" in bems_product


def filter_root_cause(root_cause):
    """Logic for generating the data for the 'Root Cause Classification for Closed Escalations' in the .ppt"""
    if "Works as Designed" in root_cause and "Insufficient Diagnostics" in root_cause:
        return "Other"
    if "Documentation" in root_cause:
        return "Documentation"
    for rc_candidate in ("Cause not Determined", "Software Defect - New", "Software Defect - Existing", "Configuration",
                         "Works as Designed", "Product does not meet customer expectations",
                         "Hardware failure", "Hardware failure", "Network / Solution Design", "Documentation", "Other"):
        if root_cause.startswith(rc_candidate):
            return rc_candidate
    for rc_candidate in ("Cause not Determined", "Software Defect - New", "Software Defect - Existing", "Configuration",
                         "Other", "Works as Designed", "Product does not meet customer expectations",
                         "Hardware failure", "Hardware failure", "Network / Solution Design"):
        if rc_candidate in root_cause:
            return rc_candidate
    return "Other"


def get_file_contents(filetype, stored_file):
    """
    :param filetype: Should be either 'xlsx' or 'csv'
    :param stored_file: type werkzeug.FileStorage
    :return: file_contents as one long string
    """
    blob = stored_file.stream.read()
    if filetype == 'xlsx':
        data_frame = pd.read_excel(blob)
        file_contents = data_frame.to_csv()
    else:
        encoding = chardet.detect(blob)['encoding']
        file_contents = blob.decode(encoding)
    return file_contents


def file_is_allowed(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS


def files_are_allowed(stored_files):
    for stored_file in stored_files:
        if not file_is_allowed(stored_file.filename):
            return False
    return True


def is_date(cell):
    month_pattern = '|^'.join(SHORT_MONTH_NAMES)
    return True if re.search(month_pattern, cell, re.IGNORECASE) else False


def is_registered(cell):
    return True if re.search(r'REG', cell, re.IGNORECASE) else False


def is_unregistered(cell):
    return False if re.search(r'REG|AGE', cell, re.IGNORECASE) else True


def add_date_to_data(index, cell, data):
    daily_data = {
        "Always": {},
        "Sometimes": {},
        "Never": {},
        "columns": []
    }
    month = re.search(r'[a-zA-Z]+', cell).group()
    date = re.search(r'\d+', cell).group()
    date_string = f'{month} {date}'
    if date_string not in data:
        data[date_string] = deepcopy(daily_data)
    data[date_string]["columns"].append(index)


def is_open_dg_store(column_indexes, row):
    closed_stores = get_closed_dg_stores()
    return "lab" not in row[column_indexes["name1"]].lower() \
           and "Dollar General" in row[column_indexes["name2"]] \
           and row[column_indexes["name1"]] not in closed_stores


def is_specified_store(column_indexes, row, store_name):
    return "lab" not in row[column_indexes["name1"]].lower() \
           and store_name.lower() in row[column_indexes["name2"]].lower()


def get_file_status(filename):
    if "close" in filename.lower():
        return "closed"
    elif "incoming" in filename.lower():
        return "incoming"
    else:
        raise NameError(f"'close' or 'incoming' NOT found in filename: {filename}")


def get_closed_dg_stores(closed_stores_filename="Closed_DG_Stores_27_May.xlsx"):
    wb = openpyxl.load_workbook(os.path.join("docs", closed_stores_filename))
    closed_sheet = wb["closed shops"]
    return [row[0].value for row in closed_sheet.rows if row[0].value]
