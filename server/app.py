#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'
@app.route('/vendors', method=['GET'])
def vendors():
    vendors= Vendor.query.all()
    vendors_data=[{
        "id": vendor.id,
        "name": vendor.name
    } for vendor in vendors]
    
    return jsonify(vendors_data)

@app.route('/vendors/<int:id>', methods=['GET'])
def vendors_by_id():
    vendor= Vendor.query.get(id)
    if vendor:
        vendor_sweet_data=[{
            "id": vs.id, 
            "price": vs.price, 
            "sweet": vs.sweet.to_dict(), 
            "sweet_id": vs.sweet_id, 
            "vendor_id": vs.vendor_id}         
          for vs in vendor.vendor_sweet]
        vendor_data={
            "id":
        }


@app.route('/sweets')
def sweets():
    pass

@app.route('/sweets/<int:id>')
def sweets_by_id():
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)
