#!/usr/bin/env python3
import os
from models import db
from models.sweet import Sweet
from models.vendor import Vendor
from models.vendor_sweet import  VendorSweet

from dotenv import load_dotenv
load_dotenv()

from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api= Api(app)


@app.route('/')
def home(): 
    return '<h1>Code Challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)