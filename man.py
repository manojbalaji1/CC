from flask import Flask, jsonify, request, make_response, json,render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import sqlalchemy
import sqlite3
from passlib.apps import custom_app_context as pwd_context

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test_database.db'

test_db= SQLAlchemy(app)
api=Api(app)



"""Table to store user details"""

class user_table(test_db.Model):
    __tablename__='User'
    index = test_db.Column(test_db.Integer, primary_key=True)
    user_name = test_db.Column(test_db.String)
    password = test_db.Column(test_db.String)
    email = test_db.Column(test_db.String)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

"""End of User table"""

"""*********************************************************************"""

"""Table to store Company details"""

class company_table(test_db.Model):
    __tablename__='company'
    index = test_db.Column(test_db.Integer, primary_key=True)
    user_name = test_db.Column(test_db.String)
    password = test_db.Column(test_db.String)
    email = test_db.Column(test_db.String)
    company_name = test_db.Column(test_db.String)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

"""end of company table"""

"""*********************************************************************"""

"""Table to store Problem"""

class Problem_table(test_db.Model):
    __tablename__='blog'
    index = test_db.Column(test_db.Integer, primary_key=True)
    Title = test_db.Column(test_db.String)
    Content = test_db.Column(test_db.String)
    Location = test_db.Column(test_db.String)
    Contact = test_db.Column(test_db.String)
"""end of problem table"""

"""*********************************************************************"""

"""Routing User signup"""

@app.route('/user_signup', methods=['POST','GET'])
def user_signup():
    reg_data= json.loads(request.data)
    print request.get_json(silent=True)
    username = reg_data.get('username')
    password = reg_data.get('password')
    email = reg_data.get('email')
    print username, password
    if check_user_signup(username):
        return 'Username not available'
    else:
        if check_user_email(email):
            return 'Email id has been already used'
        else:
            add_to_user_db(username, password, email)
            return "su"


"""End of Routing User signup function"""

"""*********************************************************************"""
@app.route('/signup_user_page', methods=['POST','GET'])
def user_signin_page():
    return render_template('user_signup.html')

@app.route('/signup_company_page', methods=['POST','GET'])
def company_signin_page():
    return render_template('company_signup.html')

@app.route('/login_company_page', methods=['POST','GET'])
def company_login_page():
    return render_template('company_login.html')


@app.route('/user_problem_page', methods=['POST','GET'])
def user_problem_page():
    return render_template('user_problem.html')

@app.route('/login_user', methods=['POST','GET'])
def user_login_page():
    return render_template('user_login.html')

@app.route('/user_problem', methods=['POST','GET'])
def user_problem():
    reg_data= json.loads(request.data)
    Title = reg_data.get('title')
    Content = reg_data.get('content')
    location = reg_data.get('location')
    contact = reg_data.get('contact')
    add_to_user_problem_db(Title, Content,location,contact)
    return 'uploaded'

"""End of Routing User problem function"""

"""*********************************************************************"""

"""routing company signup"""

@app.route('/company_signup', methods=['POST','GET'])
def company_signup():
    reg_data= json.loads(request.data)
    username = reg_data.get('username')
    password = reg_data.get('password')
    email = reg_data.get('email')
    company_name = reg_data.get('company_name')
    print username, password
    if check_company_signup(username):
        return 'Username not available'
    else:
        if check_company_email(email):
            return 'Email id has been already used'
        else:
            add_to_company_db(username, password, email, company_name)
            print("added to db")
            return "hey"
"""End of routing company signup function"""

"""*********************************************************************"""

"""Routing Login"""

@app.route('/login', methods=['POST','GET'])
def login_authenticaiton():
    login_data=json.loads(request.data)
    username = login_data.get('username')
    password = login_data.get('password')
    user_info = user_table.query.filter_by(user_name = username).all()
    for rows in user_info:
        if(rows.user_name == None):
            return 'User not found'
        if username == rows.user_name and rows.verify_password(password):
            print 'login successful'
        else:
            print 'login failed'
            return 'login failed'
        return 'login successful'

"""End of Routing Login function"""

"""*********************************************************************"""

@app.route('/login_company',methods=['POST','GET'])
def company_login():
	login_data=json.loads(request.data)
	username = login_data.get('username')
	password = login_data.get('password')
	user_info = company_table.query.filter_by(user_name = username).all()
	for rows in user_info:
		if(rows.user_name == None):
			return 'User not found'
        if rows.user_name == username  and rows.verify_password(password):
            print 'login successful'
        else:
            print 'login failed'
            return 'login failed'
        return redirect(url_for('/'))

@app.route("/")
def home():
	return render_template("index.html")

"""Post Route"""
@app.route("/show_all")
def show_all():
   return render_template('show_all.html', users = Problem_table.query.all() )
    
"""End of post Route function"""

@app.route("/show_all_user")
def show_all_user():
   return render_template('show_all_user.html', users = Problem_table.query.all() )
"""*********************************************************************"""

"""check user username redunduncy"""

def check_user_signup(un):
    user_info = user_table.query.filter_by(user_name = un).all()
    for rows in user_info:
        if un== rows.user_name:
            print 'username not available'
            return True

"""End of check user username redunduncy function"""

"""*********************************************************************"""

"""check company username redunduncy"""
def check_company_signup(un):
    user_info = company_table.query.filter_by(user_name = un).all()
    for rows in user_info:
        if un== rows.user_name:
            print 'username not available'
            return True

"""End of check company username redunduncy function"""

"""*********************************************************************"""

"""check user email redunduncy"""

def check_user_email(ut):
    user_info = user_table.query.filter_by(email = ut).all()
    for rows in user_info:
        if ut== rows.email:
            print 'email already in Use'
            return True

"""End of check user email redunduncy function"""

"""*********************************************************************"""

"""check company email redunduncy"""

def check_company_email(ut):
    user_info = user_table.query.filter_by(email = ut).all()
    for rows in user_info:
        if ut== rows.email:
            print 'email already in Use'
            return True

"""End of check company email redunduncy function"""

"""*********************************************************************"""

"""check company name redunduncy"""

def check_comany_name(cn):
    user_info = user_table.query.filter_by(company_name = cn).all()
    for rows in user_info:
        if cn == rows.company_name:
            print 'Company has Already Regsitered'
            return True

"""End of check company name redunduncy function"""

"""*********************************************************************"""

"""Add to user table"""

def add_to_user_db(un,pw,em):
    data= user_table(user_name=un,email=em)
    print(data)
    print("Adding user to db")
    data.hash_password(pw)
    test_db.session.add(data)
    test_db.session.commit()

"""end of addition"""

"""*********************************************************************"""

"""Add to company table"""

def add_to_company_db(un,pw,em,cm):
    data= company_table(user_name=un,email=em,company_name=cm)
    print(data)
    print("Adding user to db")
    data.hash_password(pw)
    test_db.session.add(data)
    test_db.session.commit()

"""end of addition"""

"""*********************************************************************"""

"""Add to User table"""

def add_to_user_problem_db(un,pw,em,ct):
    data= Problem_table(Title=un,Content=pw,Location=em,Contact=ct)
    test_db.session.add(data)
    test_db.session.commit()

"""End of addition"""

"""*********************************************************************"""

"""Running"""

if __name__=='__main__':
    test_db.create_all()
    test_db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5151)
