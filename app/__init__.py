from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from config import Config




db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login'
ckeditor = CKEditor()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app,db)
        ckeditor.init_app(app)
        
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from app.main import bp as main_bp
        app.register_blueprint(main_bp)

        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from app.blog import bp as blog_bp
        app.register_blueprint(blog_bp, url_prefix='/blog')

        from app.admin_content import bp as admin_content_bp
        app.register_blueprint(admin_content_bp, url_prefix='/admin')

        from app.admin_tag import bp as admin_tag_bp
        app.register_blueprint(admin_tag_bp, url_prefix='/admin')


    
    return app
