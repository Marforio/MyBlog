from flask import Flask

def create_app():
    app = Flask(__name__)
    with app.app_context():
        from . import intro
        app.register_blueprint(intro.intro_bp)
        return app