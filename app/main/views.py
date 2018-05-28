from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import BlogForm, CommentForm
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


@main.route('/blog/<int:id>')
def blog(id):
    blog = Blog.query.get(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content = form.content.data, comment = commet, author = current_user._get_current_object())
        db.session.add(comment)
        flash("Your comment has been published")
        return redirect(url_for('.blog', id = blog.id))
    return render_template('blog.html', blogs = [blog], comment_form = form, comment = comments)


@main.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    blog = Blog.query.get_or_404(id)
    # if current_user != post.author and \
    #     not current_user.can(Permission.ADMINISTER):
    # abort(403)
    form = BlogForm()
    if form.validate_on_submit():
        blog.content = form.content.data

        db.session.add(blog)

        flash('The blog has been updated.')

        return redirect(url_for('post', id = blog.id))
    form.content.data = blog.content
    return render_template('edit_blog.html', blog_form=form)

