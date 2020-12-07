from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor




db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login.init_app(app)
        migrate.init_app(app,db)
        ckeditor.init_app(app)
    
        from app.admin_content import bp as admin_content_bp
        app.register_blueprint(admin_content_bp, url_prefix='/admin')
    
    return app
