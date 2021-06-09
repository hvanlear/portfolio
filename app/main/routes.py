from flask import render_template, url_for, redirect, flash, request, make_response, send_file, url_for, send_from_directory
from app import db
from app.main import bp
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Project, Tag
from werkzeug.urls import url_parse


@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.order_by(Post.create_date.desc()).limit(2).all()
    projects = Project.query.all()
    for pr in projects:
        if pr.demo_link == "":
            print('hello')
    return render_template('main/index.html', title='Home', posts=posts, projects=projects)


@bp.route('/index/contact')
def contact():
    # must be a better way of doing this
    posts = Post.query.order_by(Post.create_date.desc()).limit(2).all()
    projects = Project.query.all()
    return render_template('main/index.html', posts=posts, projects=projects, scrollToAnchor="contact_section")


@bp.route('/about')
def show_about():
    return render_template('main/about.html', title='Me')


@bp.route('/resume')
def show_resume():
    return send_file('static/assets/hresume.pdf', attachment_filename='hresume.pdf')
