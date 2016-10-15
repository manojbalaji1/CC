# imports
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash,g,_app_ctx_stack
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import check_password_hash, generate_password_hash
import os
from sqlite3 import dbapi2 as sqlite3
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'gingersoda'
# USERNAME = 'admin'
# PASSWORD = 'admin'
sqlite3.connect(os.path.abspath("flaskr.db"))
# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

# the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

# create app
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(__name__)
db = SQLAlchemy(app)

import models
@app.route('/', methods=['GET', 'POST'])   # pragma: no cover
@login_required   # pragma: no cover
def home():
    error = None
    form = models.MessageForm(request.form)
    if form.validate_on_submit():
        new_message = models.BlogPost(
            form.title.data,
            form.description.data,
            current_user.id
        )
        db.session.add(new_message)
        db.session.commit()
        flash('New entry was successfully posted. Thanks.')
        return redirect(url_for('home'))
    else:
        posts = db.session.query(models.BlogPost).all()
        return render_template(
            'index1.html', posts=posts, form=form, error=error)


@app.route("/logout")
@login_required
def logout():
    session.pop('user_id', None)
    logout_user()
    return redirect(url_for('welcome'))


@app.route('/register', methods=['GET', 'POST'])   # pragma: no cover
def register():
    form = models.RegisterForm()
    if form.validate_on_submit():
        user = models.User(
            name=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])   # pragma: no cover
def login():
    error = None
    form = models.LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = models.User.query.filter_by(name=request.form['username']).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, request.form['password']
            ):
                login_user(user)
                flash('You were logged in. Go Crazy.')
                return redirect(url_for('home'))

            else:
                error = 'Invalid username or password.'
    return render_template('login1.html', form=form, error=error)


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter(models.User.id == int(user_id)).first()


if __name__=='__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5151)
