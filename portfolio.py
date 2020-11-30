from app import app, db
from app.models import User, Post, Project, Tag, Post_Tag, Project_Tag


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
