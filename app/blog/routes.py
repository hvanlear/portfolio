from app import db
from app.models import Post, Tag
from app.blog import bp
from app.helpers import object_list
from flask import render_template, redirect, request, url_for,flash
from app.blog.forms import PostForm
from flask_login import current_user,login_required

@bp.route('/')
def blog_index():
    posts = Post.query.order_by(Post.create_date.desc())
    return object_list('blog/blog_index.html', posts)

@bp.route('/tags/')
def blog_tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('blog/tag_index.html', tags)

@bp.route('/tags/<slug>/')
def blog_tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    posts = tag.posts.order_by(Post.create_date.desc())
    return object_list('blog/tag_detail.html', posts, tag=tag )

#add current user to the new Post route

@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create_blog_post():
    if request.method == 'POST':
        form = PostForm(request.form)
        if form.validate_on_submit():
                post = Post(title=form.title.data,
                            body=form.body.data, tags=form.tags.data)
                db.session.add(post)
                db.session.commit()
                flash('Post Submitted')
                return redirect(url_for('blog.detail', slug=post.slug))
    else:
        form = PostForm()

    return render_template('blog/create_blog_post.html', form=form)

@bp.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if request.method == "POST":
        form = PostForm(request.form, obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            post.tags = form.tags.data
            db.session.add(post)
            db.session.commit()
            flash('post updated')
            return redirect(url_for('blog.detail', slug=post.slug))
        elif request.method == 'GET':
            form.title.data = post.title
            form.body.data = post.body
            form.tags.data = post.tags
    else:
        form = PostForm(obj=post)
    
    return render_template('/blog/edit_post.html', post=post, form=form)

@bp.route('/<slug>/')
def detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('blog/detail.html', post=post)

@bp.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete_blog_post(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    if post is None:
        flash('No Such Post')
        return redirect(url_for('blog.blog_index'))
    db.session.delete(post)
    db.session.commit()
    flash('post deleted')
    return redirect(url_for('blog.blog_index'))