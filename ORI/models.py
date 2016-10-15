from app import db
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField
from wtforms import TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional
from wtforms.validators import Length, Email

class Flaskr(db.Model):

    __tablename__ = "flaskr"

    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    post_id = db.Column(db.Integer,autoincrement=True)
    title = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    pw_hash = db.Column(db.String, nullable=False)
    agree = db.Column(db.Boolean, nullable=False)

    def __init__(self, title, text, username, email, pw_hash, agree):
        self.title = title
        self.text = text
        self.username = username
        self.email = email
        self.pw_hash = pw_hash
        self.agree = agree

    def __repr__(self):
        return '<title {}>'.format(self.body)
