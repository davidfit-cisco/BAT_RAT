from flask import render_template, request, flash
from models.rat import RegistrationAnalysisTool
from utils.utils import file_is_allowed, ALLOWED_EXTENSIONS


def rat_page(app):
    """
    If the method is a simple GET request for /rat then the rat.html page will simply be rendered. If there are any
    errors on the page (as indicated by the Flask "flash" method, then the errors will be rendered on the rat.html page.

    If the method is a POST request then we assume files are being sent to the server (but only used in memory,
    to be safe they are not saved to the server) for processing.

    First we get the file that has been sent in through file_upload.html

    We then initialise the RAT tool which does the backend processing of the csv/xlsx files to return the data we need
    to display.

    The data is then sent to the rat_processed.html template file where the python data can be inter-weaved into the
    simple html tables.
    """
    if request.method == 'POST':
        store_name = request.form.get("store_name")
        if store_name is None:
            store_name = "Dollar General"
        upload_files = request.files.to_dict(flat=False)["upload_files"]
        if len(upload_files) != 1:
            flash("You must select EXACTLY 1 file")
        stored_file = upload_files[0]
        if not file_is_allowed(stored_file.filename):
            flash(f"Filetype {stored_file.content_type} not allowed")
            flash(f"Allowed filetypes are: {', '.join(list(ALLOWED_EXTENSIONS))}")
        else:
            rat = RegistrationAnalysisTool(stored_file, store_name=store_name)
            main_data, tcp_data, tcp_never_macs, days = rat.get_data()
            return render_template('rat_processed.html',
                                   main_data=main_data, tcp_data=tcp_data,
                                   tcp_never_macs=tcp_never_macs, days=list(main_data.keys()))
    return render_template('rat.html')

