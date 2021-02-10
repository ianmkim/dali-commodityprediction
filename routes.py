import hashlib
from app import *

from flask import Response, jsonify
import os, json
import datetime
import requests

from flask import Flask,send_file,  request, redirect, url_for
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup

from sqlalchemy import desc

@app.route('/')
@app.route('/index')
def index():
    return "prediction engine v2.2"
