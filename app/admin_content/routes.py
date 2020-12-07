from flask import render_template, url_for, redirect, flash, request
from app import  db
from app.admin_content.forms import PostForm, EditPost
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Tag
from werkzeug.urls import url_parse
from app.admin_content import bp



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