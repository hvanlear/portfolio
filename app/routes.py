from flask import render_template, url_for, redirect, flash, request
from app import app, db
from app.forms import LoginForm, PostForm, EditPost
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.create_date.desc()).limit(2).all()
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login-admin', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login-admin'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# route is undeed, functionality rolled into /admin-panel


# @app.route('/post', methods=['GET', 'POST'])
# @login_required
# def post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data,
#                     body=form.body.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Post Submitted')
#         return redirect(url_for('index'))
#     return render_template('post.html', form=form)


@app.route('/admin-panel', methods=['GET', 'POST'])
@login_required
def admin_panel():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Submitted')
        return redirect(url_for('admin_panel'))
    posts = Post.query.order_by(Post.create_date.desc()).all()
    return render_template('admin_panel.html', posts=posts, form=form)


@app.route('/admin-panel/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    post = Post.query.get(post_id)
    if post is None:
        flash('No Such Post')
        return redirect(url_for('index'))

    form = EditPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('post updated')
        return redirect(url_for('admin_panel'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit_post.html', form=form, post=post)


@app.route('/admin-panel/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('No Such Post')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin_panel'))
