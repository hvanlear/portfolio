from flask import render_template, url_for, redirect, flash, request
from app import  db
from app.admin_content.forms import PostForm, EditPost
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Tag
from werkzeug.urls import url_parse
from app.admin_content import bp



@bp.route('/admin-panel', methods=['GET', 'POST'])
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

@bp.route('/admin-panel/<int:post_id>', methods=['GET', 'POST'])
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
    return render_template('admin_content/edit_post.html', form=form, post=post)


@bp.route('/admin-panel/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('No Such Post')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin_content/admin_panel'))

# @bp.route('/admin-panel/add-project', methods=['GET', 'POST'])
# @login_required
# def add_project():


#     form = AddProject()
#     form.tags.choices = [(t.id, t.name) for t in Tag.query.all()]
 
#     if form.validate_on_submit():
#         project = Project(title=form.title.data,
#                           about=form.about.data, demo_link=form.demo_link.data, github_link=form.github_link.data)
#         db.session.add(project)
#         db.session.commit()
#         flash('Project Added')
#         return redirect(url_for('admin_panel'))
#     return render_template('add_project.html', form=form)