from flask import Flask, jsonify, request, make_response, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Resource, Api
import sqlalchemy
import sqlite3
from passlib.apps import custom_app_context as pwd_context

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test_database.db'

test_db= SQLAlchemy(app)
api=Api(app)

class first_table(test_db.Model):
    __tablename__='registration'
    index = test_db.Column(test_db.Integer, primary_key=True,autoincrement=True)
    user_name = test_db.Column(test_db.String)
    password = test_db.Column(test_db.String)
    email = test_db.Column(test_db.String)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


@app.route('/signup', methods=['POST','GET'])
def signup():
    reg_data= json.loads(request.data)
    username = reg_data.get('username')
    password = reg_data.get('password')
    email = reg_data.get('email')
    print username, password
    if check_signup(username):
        return 'Username not available'
    else:
        if check_email(email):
            return 'Email id has been already used'
        else:
            add_to_db(username, password, email)
            return 'Signup Successful'
