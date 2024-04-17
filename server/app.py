#!/usr/bin/env python3
from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource, abort
from sqlalchemy.orm.exc import NoResultFound
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

class Home(Resource):

    def get(self):        
        response_dict = {
            "message": "Code challenge",
        }       
        response = make_response(
            response_dict,
            200,
        )
        return response

class Vendors(Resource):
    def get(self):
        vendors=[{"id": vendor.id, "name": vendor.name} for vendor in Vendor.query.all()]
        response = make_response(
            vendors,
            200,
        )
        return response

class VendorById(Resource):
    def get(self, id):
        vendor = Vendor.query.filter_by(id=id).first()
        if vendor:        
            vendor_data = {
                'id': vendor.id,
                'name': vendor.name,
                'vendor_sweets': [
                    {
                        'id': vs.id,
                        'price': vs.price,
                        'sweet': {'id': vs.sweet.id, 
                                  'name': vs.sweet.name},
                        'sweet_id': vs.sweet.id,
                        'vendor_id': vs.vendor.id
                    } for vs in vendor.vendor_sweets
                ]
            }
            return jsonify(vendor_data)
        else:
            return jsonify({'error': 'Vendor not found'}),404

class Sweets(Resource):

    def get(self):
        sweets = Sweet.query.all()
        sweets_data = [{
            "id": sweet.id, 
            "name": sweet.name} for sweet in sweets]
        return jsonify(sweets_data)

class SweetsById(Resource):
    def get(self, id):
        sweet = Sweet.query.filter_by(id=id).first()
        if sweet:            
            return jsonify({"id": sweet.id, "name": sweet.name})
        else:
            jsonify({"error": "Sweet not found"}), 404

class VendorSweets(Resource):
    def post(self):
        vendor_sweet_data=request.get_json()
        price= vendor_sweet_data.get("price")
        vendor_id=vendor_sweet_data.get("vendor_id")
        sweet_id=vendor_sweet_data.get("sweet_id")

        

        if not all([price, vendor_id, sweet_id]):
            return jsonify({"error": "validation error"}), 400
        
        try:
            vendor=Vendor.query.filter_by(id=vendor_id).one()
            sweet= Sweet.query.filter_by(id=sweet_id).one()
        except NoResultFound:
            return jsonify({"errors": "Vendor or sweet not found"}), 404
        
        vendor_sweet=VendorSweet(price=price, vendor=vendor, sweet=sweet)
        db.session.add(vendor_sweet)
        db.session.commit()

        response_data = {
            "id": vendor_sweet.id,
            "price": vendor_sweet.price,
            "sweet": {"id": sweet.id, "name": sweet.name},
            "sweet_id": sweet.id,
            "vendor": {"id": vendor.id, "name": vendor.name},
            "vendor_id": vendor.id
        }
        return jsonify(response_data), 201
    
class VendorSweetsResource(Resource):
    def delete(self, id):
        vendor_sweet=VendorSweet.query.filter_by(id=id).first()
        if vendor_sweet:
            db.session.delete(vendor_sweet)
            db.session.commit()
            return {}, 204
        else:
            return jsonify({"error": "VendorSweet not found"}), 204    

api.add_resource(Home, '/')
api.add_resource(Vendors, '/vendors')
api.add_resource(VendorById, '/vendors/<int:id>')
api.add_resource(Sweets, '/sweets')
api.add_resource(SweetsById, '/sweets/<int:id>')
api.add_resource(VendorSweets, '/vendor_sweets')
api.add_resource(VendorSweetsResource, '/vendor_sweets/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
