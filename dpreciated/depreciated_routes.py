from flask import render_template, url_for, redirect, flash, request
from app import  db
from app.forms import LoginForm, PostForm, EditPost, AddProject
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Project, Tag, Project_Tag
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.create_date.desc()).limit(2).all()
    projects = Project.query.all()
    return render_template('index.html', title='Home', posts=posts, projects=projects)


@app.route('/blog')
def show_all_posts():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)


@app.route('/about')
def show_about():
    return render_template('about.html', title='Me')


@app.route('/admin-login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin-login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)




# route not needed, functionality rolled into /admin-panel


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


@app.route('/admin-panel/add-project', methods=['GET', 'POST'])
@login_required
def add_project():


    form = AddProject()
    form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
 
    if form.validate_on_submit():
        project = Project(title=form.title.data,
                          about=form.about.data, demo_link=form.demo_link.data, github_link=form.github_link.data)
        db.session.add(project)
        db.session.commit()
        flash('Project Added')
        return redirect(url_for('admin_panel'))
    return render_template('add_project.html', form=form)


