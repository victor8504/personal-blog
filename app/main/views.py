from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import User
from flask_login import login_required
from .. import db
import markdown2

@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'PERSONAL BLOG'

    return render_template('index.html', title = title)