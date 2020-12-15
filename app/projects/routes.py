from app import db
from app.models import Project, Tag
from app.projects import bp
from app.helpers import object_list
from flask import render_template, redirect, request, url_for,flash
from app.projects.forms import ProjectForm
from flask_login import current_user


@bp.route('/')
def project_index():
    projects = Project.query.order_by(Project.title.desc())
    return object_list('projects/project_index.html', projects)

@bp.route('/tags/')
def project_tags_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('projects/project_tags_index.html', tags)

@bp.route('/tags/<slug>/')
def project_tags_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    projects = tag.projects.order_by(Project.title.desc())
    return object_list('projects/project_tags_detail.html', projects, tag=tag )

#add current user to the new Post route

@bp.route('/create/', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        form = ProjectForm(request.form)
        if form.validate_on_submit():
                project = Project(title=form.title.data,
                            about=form.about.data, demo_link = form.demo_link.data, github_link = form.github_link.data, tags=form.tags.data)
                db.session.add(project)
                db.session.commit()
                flash('project Submitted')
                return redirect(url_for('projects.project_index', slug=project.slug))
    else:
        form = ProjectForm()

    return render_template('projects/add_project.html', form=form)


@bp.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    project = Project.query.filter(Project.slug == slug).first_or_404()
    if request.method == "POST":
        form = ProjectForm(request.form, obj=project)
        if form.validate_on_submit():
            project.title = form.title.data
            project.about = form.about.data
            project.tags = form.tags.data
            db.session.add(project)
            db.session.commit()
            flash('project updated')
            return redirect(url_for('projects.project_index', slug=project.slug))
        elif request.method == 'GET':
            form.title.data = project.title
            form.about.data = project.about
            form.tags.data = project.tags
    else:
        form = ProjectForm(obj=project)
    
    return render_template('/projects/project_edit.html', project=project, form=form)

@bp.route('/<slug>/')
def detail(slug):
    project = Project.query.filter(Project.slug == slug).first_or_404()
    return render_template('blog/detail.html', project=project)