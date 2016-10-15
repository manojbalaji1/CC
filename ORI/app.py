# imports
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash,g,_app_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import check_password_hash, generate_password_hash
import os
from sqlite3 import dbapi2 as sqlite3
import json


# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# create app
app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from models import *

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db



def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = query_db('select user_id from flaskr where username = ?',
                  [username], one=True)
    return rv[0] if rv else None

def get_email_id(email):
    """Convenience method to look up the id for a email."""
    rv = query_db('select user_id from flaskr where email = ?',
                  [email], one=True)
    return rv[0] if rv else None


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from flaskr where user_id = ?',
                          [session['user_id']], one=True)



@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    entries = db.session.query(models.Flaskr)
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = models.Flaskr(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management."""
    error = None
    if request.method == 'POST':
        user = query_db('''select * from flaskr where
            username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user['pw_hash'],request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(models.Flaskr).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return result

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = Flaskr(request.form)
        if form.validate():
            user = flaskr()
            form.populate_obj(user)
            user_exist = Users.query.filter_by(username=form.username.data).first()
            email_exist = Users.query.filter_by(email=form.email.data).first()
            if user_exist:
                form.username.errors.append('Username already taken')
            if email_exist:
                form.email.errors.append('Email already use')
            if user_exist or email_exist:
                return render_template('signup.html', form = form, page_title = 'Signup to Bio Application')
    return render_template('signup.html', form = Flaskr(), page_title = 'Signup to Bio Application')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
