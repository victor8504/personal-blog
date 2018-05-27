from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import BlogForm
from ..models import User, Blog
from flask_login import login_required
from .. import db
import markdown2

# @main.route('/')
# @login_required
# def index():

#     '''
#     View root page function that returns the index page and its data
#     '''

#     title = 'PERSONAL BLOG'

#     return render_template('index.html', title = title)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = BlogForm()

    # if current_user.can(Permission.WRITE_ARTICLES) and \
    if form.validate_on_submit():
        title = form.title.data
        blog = form.content.data

        # author = current_user._get_current_object()

        db.session.add(blog)

        return redirect(url_for('.index'))

    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('index.html', blog_form = form, blogs = blogs)

