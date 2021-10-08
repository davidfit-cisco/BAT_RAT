from flask import render_template, request, flash
from models.bat import BEMSAnalysisTool
from utils.utils import files_are_allowed, ALLOWED_EXTENSIONS


def bat_page(app):
    """
    If the method is a simple GET request for /bat then the bat.html page will simply be rendered. If there are any
    errors on the page (as indicated by the Flask "flash" method, then the errors will be rendered on the bat.html page.

    If the method is a POST request then we assume files are being sent to the server (but only used in memory,
    to be safe they are not saved to the server) for processing.

    First we get the two upload files, that have been sent in through file_upload.html

    We then initialise the BAT tool which does the backend processing of the csv/xlsx files to return the data we need
    to display.

    The data is then sent to the bat_processed.html template file where the python data can be inter-weaved into the
    simple html tables.
    """
    if request.method == "POST":
        upload_files = request.files.to_dict(flat=False)["upload_files"]
        if len(upload_files) != 2:
            flash("You must select EXACTLY 2 files")
        elif not files_are_allowed(upload_files):
            names = [stored_file.filename for stored_file in upload_files]
            flash(f"At least one filetype in {', '.join(names)} is not allowed")
            flash(f"Allowed filetypes are: {', '.join(list(ALLOWED_EXTENSIONS))}")
        else:
            bat = BEMSAnalysisTool()
            enterprise_data, mpp_data = bat.get_data(upload_files)
            return render_template('bat_processed.html', enterprise_data=enterprise_data, mpp_data=mpp_data)
    return render_template("bat.html")
