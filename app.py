from flask import Flask
from assets import register_assets


# Entry point to application
def create_app():
    reg_state_app = Flask(__name__)
    reg_state_app.secret_key = 'secret'
    with reg_state_app.app_context():
        import routes  # Contrary to PEP, this import here is vital
        register_assets()
    return reg_state_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
