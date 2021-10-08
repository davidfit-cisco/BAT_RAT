from flask import Flask


def create_app():
    """
    Entry point to application.
    Open the routes file to see what methods are called when a user visits a certain route (/bat or /rat)
    """
    reg_state_app = Flask(__name__)
    reg_state_app.secret_key = 'secret'
    with reg_state_app.app_context():
        import routes  # Contrary to PEP, this import here is vital
    return reg_state_app


if __name__ == '__main__':
    """This creates the app and runs the file, host=0.0.0.0 makes the server accessible to anybody. Note, I have had 
    some weird requests come in to the server from some public 173.xxx.xxx.xxx address trying to exploit an issue with 
    Oracle WebLogic. But this should not be a real problem since WebLogic is not used.
    
    I wasn't sure how to whitelist/blacklist IPs at this stage."""
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=8000)
