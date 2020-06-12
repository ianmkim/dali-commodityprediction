from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
#from flask_login import current_user, login_required, login_user, logout_user
#from flask_cors import CORS, cross_origin 

from flask import redirect,jsonify, url_for, render_template, request

#from flask_wtf import FlaskForm
#from wtforms import IntegerField,SelectField, StringField, PasswordField, BooleanField, SubmitField
#from wtforms.validators import ValidationError,DataRequired, Email, EqualTo
#from flask_bcrypt import Bcrypt

#from flask_compress import Compress
#import flask_whooshalchemy as wa

from flask_sslify import SSLify
from jinja2 import Environment, FileSystemLoader ,PackageLoader, select_autoescape

#from flask_mail import Mail, Message

#import flask_login

import oracle

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SECRET_KEY'] = 'saomehteuhufebubceisucdbue'
app.config['SECURITY_PASSWORD_SALT'] = 'My_PRECEIOUS_SALTING_THINGrungbur'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_arr =request.form.getlist('slice[]')
    #test_arr = [28.33, 28.34, 28.32, 28.3, 28.32, 28.27, 28.29, 28.34, 28.3, 28.33] # answer should be 28.18
    print("\n\n\n\n\n\n", input_arr)
    pred1 = oracle.predict_next_price(input_arr)[0][0]
    input_arr.pop(0)
    input_arr.append(pred1)
    pred2 = oracle.predict_next_price(input_arr)[0][0]
    return str([pred1, pred2])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
