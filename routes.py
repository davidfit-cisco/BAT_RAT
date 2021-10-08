from flask import current_app, redirect, url_for
from controllers.bat import bat_page
from controllers.rat import rat_page


@current_app.route('/', methods=['GET', 'POST'])
def home():
    """Simply redirect to /bat as the homepage"""
    return redirect(url_for("bat"))


@current_app.route('/bat', methods=['GET', 'POST'])
def bat():
    """Render the bat_page"""
    return bat_page(current_app)


@current_app.route('/rat', methods=['GET', 'POST'])
def rat():
    """Render the rat_page"""
    return rat_page(current_app)

