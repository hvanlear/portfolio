from app import create_app, db
from app.models import User, Post, Project, Tag, post_tags

app = create_app()
#run inside of ipyton to create context for commands inside
# app.app_context().push()

with app.app_context():
    #it seems you need to wrap it inside with app.app_context otherwise current_app is null?
    from app.models import User, Post, Tag, post_tags
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Post': Post,
                'Tag': Tag}