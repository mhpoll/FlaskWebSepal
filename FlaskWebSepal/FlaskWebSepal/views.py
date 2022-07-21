from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
 
from FlaskWebSepal import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app.config['SECRET_KEY'] = 'fb93246348ed383a9de5b7e77ff8d579' # be sure to use only the most recent key generated
#name of the database to create or use
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site2.db'

db = SQLAlchemy(app)

def newFunction(length, width, p_length, p_width): #from registration form
    df = pd.DataFrame({"Sepal Length": [length],
                     
                   "Sepal Width": [width],
                     
                   "Petal Length": [p_length],
                   
                   "Petal Width": [p_width]})
 
    print("Original DataFrame :", df)
    
    df.to_csv('data.csv')
    
    html=df.to_html()
    
    text_file = open("C:\\Users\\Mitchell's Build 1\\source\\repos\\FlaskWebSepal\\FlaskWebSepal\\FlaskWebSepal\\templates\\\mitchell.html", "w")
    text_file.write('{% extends "layout.html" %}')
    text_file.write('\n''{% block content %}' '\n')
    text_file.write('\n''<div class="jumbotron">'
                    '\n''<h1>Results</h1>'
                    '\n''<p class="lead">Flower Dimensions.</p>'
                    '\n''<p><a href="{{ url_for("register") }}">Enter New Values </a></p>'
                    '\n''</div>')
    text_file.write(html)
    text_file.write('\n''{% endblock content %}')
    text_file.close()
 


#Because of __tablename__ database table is 'usertable"
class User(db.Model):
  __tablename__ = 'valuetable' #if do not specify the table name is user
  id = db.Column(db.Integer, primary_key=True)
  length = db.Column(db.Integer(), nullable=False)
  width = db.Column(db.Integer(), nullable=False)
  p_length = db.Column(db.Integer(), nullable=False)
  p_width = db.Column(db.Integer(), nullable=False)

  def __repr__(self):
    return f"usertable('{self.username}', '{self.email}', '{self.password}')"


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/mitchell')
def mitchell():
    """Renders the dynamic page."""
    return render_template(
        'mitchell.html',
        title='Mitchell',
        year=datetime.now().year,
        message='Dynamic page.'
    )

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if request.method == 'POST' and form.validate():
            newFunction(form.length.data, form.width.data,form.p_length.data, form.p_width.data)
            '''
            db.session.add(user_a)
            db.session.commit()
            flash(f'Account created for {form.username.data}!', 'success')
            '''
            return redirect(url_for('mitchell'))
    return render_template('register.html', title='Register', year=datetime.now().year,
        message='Your register description page.',form=form)

class RegistrationForm(FlaskForm):
    length = IntegerField('Sepal Length')

    width = IntegerField('Sepal Width')

    p_length = IntegerField('Petal Length')

    p_width= IntegerField('Petal Width')
                                     
    submit = SubmitField('Submit Values')  

def readDB():
    engine = create_engine('sqlite:///site2.db', echo=False)
    connection = engine.connect()
    metadata = db.MetaData()
    print(metadata)
     
    #utable = db.Table('usertable', metadata, autoload=True, autoload_with=engine)
    query = 'show tables'
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    ResultSet[:3]  



#database, new code added to make sure table named usertable is created
db.create_all()

