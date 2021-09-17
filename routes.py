from flask import current_app, render_template


@current_app.route('/', methods=['GET', 'POST'])
def uploadfile():
    return "Homepage"


@current_app.route('/test')
def test():
    return render_template("test.html")
