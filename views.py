from flask import Flask, jsonify, request, make_response, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Resource, Api
import sqlalchemy
import sqlite3
from passlib.apps import custom_app_context as pwd_context

from man1 import *

@app.route('/signup', methods=['POST'])
def signup():
    reg_data= json.loads(request.data)
    username = reg_data.get('username')
    password = reg_data.get('password')
    username = reg_data.get('email')
    print username, password, email
    if check_signup(username):
        return 'Username not available'
    else:
        if check_email(email):
            return 'Email is already taken'
        else:
            add_to_db(username, password,email)
            return 'Signup Successful'
    return render_template('signup.html')


def check_signup(un):
    user_info = first_table.query.filter_by(user_name = un).all()
    for rows in user_info:
        if un== rows.user_name:
            print 'username not available'
            return True

def add_to_db(un,pw):
    data= first_table(user_name=un)
    data.hash_password(pw)
    test_db.session.add(data)
    test_db.session.commit()


@app.route('/login', methods=['GET'])
def login_authenticaiton():
    login_data=json.loads(request.data)
    username = login_data.get('username')
    password = login_data.get('password')
    user_info = first_table.query.filter_by(user_name = username).all()
    for rows in user_info:
        if(rows.user_name == None):
            return 'User not found'
        if username == rows.user_name and rows.verify_password(password):
            return render_template('index')
        else:
            flash('login failed')
            return 'login failed'
        return 'login successful'
    return render_template('login.html')


@app.route('/add', methods=['POST'])
def add_entry():
    """Adds new post to the database."""
    if not session.get('logged_in'):
        abort(401)
    new_entry = first_table(request.form['title'], request.form['text'])
    db.session.add(new_entry)
    db.session.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))


@app.route('/delete/<int:post_id>', methods=['GET'])
def delete_entry(post_id):
    """Deletes post from database"""
    result = {'status': 0, 'message': 'Error'}
    try:
        new_id = post_id
        db.session.query(first_table).filter_by(post_id=new_id).delete()
        db.session.commit()
        result = {'status': 1, 'message': "Post Deleted"}
        flash('The entry was deleted.')
    except Exception as e:
        result = {'status': 0, 'message': repr(e)}
    return result
