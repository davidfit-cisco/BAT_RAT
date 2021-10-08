from models.spreadsheet_reader import SpreadsheetReader
from utils.utils import filter_root_cause, get_file_contents, is_mpp, get_file_status


class BEMSAnalysisTool:
    """
    TODO
    """
    def __init__(self):
        self.escalations = {
            "mpp": {
                "closed": {"total": 0}, "incoming": {"total": 0}
            },
            "enterprise": {
                "closed": {"total": 0}, "incoming": {"total": 0}
            }
        }
        self.root_causes = {
            "mpp": {
                "Software Defect - New": 0,
                "Software Defect - Existing": 0,
                "Configuration": 0,
                "Works as Designed": 0,
                "Cause not Determined": 0,
                "Product does not meet customer expectations": 0,
                "Hardware failure": 0,
                "Network / Solution Design": 0,
                "Documentation": 0,
                "Other": 0
            },
            "enterprise": {
                "Software Defect - New": 0,
                "Software Defect - Existing": 0,
                "Configuration": 0,
                "Works as Designed": 0,
                "Cause not Determined": 0,
                "Product does not meet customer expectations": 0,
                "Hardware failure": 0,
                "Network / Solution Design": 0,
                "Documentation": 0,
                "Other": 0
            }
        }
        self.severities = {
            "mpp": {
                "Urgent": 0, "Non Urgent": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0, "total": 0
            },
            "enterprise": {
                "Urgent": 0, "Non Urgent": 0, "P1": 0, "P2": 0, "P3": 0, "P4": 0, "total": 0
            }
        }

    def device_data(self, device_type):
        return {"escalations": self.escalations[device_type],
                "root_causes": self.root_causes[device_type],
                "severities": self.severities[device_type]}

    def get_data(self, upload_files):
        """
        For each file, we will just dump the file contents into memory for processing, since they are small enough
        to do so.

        Each file is processed, the results are stored in this classes escalations, root_causes & severities dicts
        (see __init__ above) and then data is returned both for enterprise and mpp.
        """
        for stored_file in upload_files:
            filename = stored_file.filename
            filetype = filename.split(".")[-1]
            self.process_file(filename, file_contents=get_file_contents(filetype, stored_file))
        return self.device_data("enterprise"), self.device_data("mpp")

    def process_file(self, filename, file_contents):
        spreadsheet = SpreadsheetReader(filename, file_contents)
        file_status = get_file_status(filename)
        for row in spreadsheet.rows[1:]:
            device_type = "enterprise"
            bems_product = spreadsheet.get_cell(row, "BEMS Product")
            if is_mpp(bems_product):
                device_type = "mpp"
            self.classify_escalation(bems_product, device_type, file_status)
            if file_status == "incoming":
                self.classify_severity(device_type, row, spreadsheet)
            elif file_status == "closed":
                self.classify_root_cause(device_type, row, spreadsheet)

    def classify_escalation(self, bems_product, device_type, file_status):
        """
        Logic for generating the data for the 'Breakdown of Escalations by Phone Model' used in the .ppt file
        """
        if bems_product not in self.escalations[device_type][file_status]:
            self.escalations[device_type][file_status][bems_product] = 0
        self.escalations[device_type][file_status][bems_product] += 1
        self.escalations[device_type][file_status]["total"] += 1

    def classify_root_cause(self, device_type, row, spreadsheet):
        """
        Logic for generating the data for the 'Root Cause Classification for Closed Escalations' used in the .ppt file
        """
        root_cause = spreadsheet.get_cell(row, "Root Cause(s)")
        filtered_root_cause = filter_root_cause(root_cause)
        if filtered_root_cause is not None:
            self.root_causes[device_type][filtered_root_cause] += 1

    def classify_severity(self, device_type, row, spreadsheet):
        """
        Logic for generating the data for the 'Incoming Escalations Severity' used in the .ppt file
        """
        urgency = spreadsheet.get_cell(row, "Escalation Urgency")
        priority = spreadsheet.get_cell(row, "SR Priority")
        for urgency_type in ("Urgent", "Non Urgent"):
            if urgency == urgency_type:
                self.severities[device_type][urgency_type] += 1
        if len(priority) > 0:
            self.severities[device_type][f"P{priority[0]}"] += 1
            self.severities[device_type]["total"] += 1


