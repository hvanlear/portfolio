from app import db, login_manager
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post_Tag(db.Model):
    __tablename__ = 'post_tag'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(15000), nullable=False)
    update_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Post_Tag',foreign_keys=[Post_Tag.post_id], \
                                    backref=db.backref('posts',lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')
    
    def getPost(self, id):
        return Post.query.filter(Post.id==id).first()
    
    def getPostBySlug(self, slug):
        return Post.query.filter(Post.slug==slug).first()
    
        #return a list of tag names for this post
    def getTagNames(self):
        tags = Tag.query.filter(Tag.posts.any(post_id=self.id)).all()
        return [tag.name for tag in tags]

    #return a string of tag names for this post
    def getTagNamesStr(self):
        return ','.join(self.getTagNames())



class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    posts = db.relationship('Post_Tag',foreign_keys=[Post_Tag.tag_id], \
                                backref=db.backref('tags',lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    
    @classmethod
    def getTagid(self, tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return -1
        else:
            return tag.id
            
    @classmethod
    def getTag(self, tag_id):
        return Tag.query.filter_by(id=tag_id).first()


class Project_Tag(db.Model):
    __tablename__ = 'project_tag'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id'), nullable=False)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(1000), nullable=False)
    demo_link = db.Column(db.String(150), nullable=True)
    github_link = db.Column(db.String(150), nullable=True)
    tags = db.relationship(
        'Tag', secondary='project_tag', backref='projects')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
