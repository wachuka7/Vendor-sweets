#!/usr/bin/env python3
import os
from models import db, Sweet, Vendor, VendorSweet

from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from sqlalchemy.orm.exc import NoResultFound

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ['postgresql://deployment_qcv4_user:JXPLm3vUkdGKjyIfiJzCVszrDXR5Siak@dpg-cof99jq1hbls7399aung-a.oregon-postgres.render.com/vendor_sweet_db']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://deployment_qcv4_user:JXPLm3vUkdGKjyIfiJzCVszrDXR5Siak@dpg-cof99jq1hbls7399aung-a.oregon-postgres.render.com/vendor_sweet_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api= Api(app)

@app.route('/')
def home(): 
    return '<h1>Code Challenge</h1>'

class VendorsResource(Resource):
    def get(self):
        vendors = Vendor.query.all()
        vendors_data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
        return jsonify(vendors_data)

class VendorResource(Resource):
    def get(self, vendor_id):
        try:
            vendor = Vendor.query.filter_by(id=vendor_id).one()
            vendor_data = {
                'id': vendor.id,
                'name': vendor.name,
                'vendor_sweets': [
                    {
                        'id': vendor_sweet.id,
                        'price': vendor_sweet.price,
                        'sweet': {'id': vendor_sweet.sweet.id, 'name': vendor_sweet.sweet.name},
                        'sweet_id': vendor_sweet.sweet_id,
                        'vendor_id': vendor_sweet.vendor_id
                    } for vendor_sweet in vendor.vendor_sweets]
            }
            return jsonify(vendor_data)
        except NoResultFound:
            response = {'error': 'Vendor not found'}
            return make_response(jsonify(response), 404)
class SweetsResource(Resource):

    def get(self):
        sweets = Sweet.query.all()
        sweets_data = [{
            "id": sweet.id, 
            "name": sweet.name} for sweet in sweets]
        return jsonify(sweets_data)

class SweetResource(Resource):
    def get(self, sweet_id):
        try:
            sweet = Sweet.query.filter_by(id=sweet_id).one()
            sweet_data = {'id': sweet.id, 'name': sweet.name}
            return jsonify(sweet_data)
        except NoResultFound:
            response = {'error': 'Sweet not found'}
            return make_response(jsonify(response), 404)

class VendorSweetResource(Resource):
    def post(self):
        vendor_sweet_data = request.get_json()
        price = vendor_sweet_data.get("price")
        vendor_id = vendor_sweet_data.get("vendor_id")
        sweet_id = vendor_sweet_data.get("sweet_id")

        errors = []

        if None in (price, vendor_id, sweet_id):
            errors.append('price, vendor_id, and sweet_id are required')

        # Validating price to ensure it's non-negative
        if price is not None and price < 0:
            errors.append('validation errors')

        if errors:
            response = jsonify({'errors': errors})
            return make_response(response, 400)

        try:
            vendor = Vendor.query.filter_by(id=vendor_id).one()
            sweet = Sweet.query.filter_by(id=sweet_id).one()

            new_vendor_sweet = VendorSweet(price=price, vendor_id=vendor.id, sweet_id=sweet.id)
            db.session.add(new_vendor_sweet)
            db.session.commit()

            vendor_sweet_data = {
                'id': new_vendor_sweet.id,
                'price': new_vendor_sweet.price,
                'sweet': {'id': sweet.id, 'name': sweet.name},
                'sweet_id': sweet.id,
                'vendor': {'id': vendor.id, 'name': vendor.name},
                'vendor_id': vendor.id
            }

            response = jsonify(vendor_sweet_data)
            return make_response(response, 201)
        except NoResultFound:
            response = {'error': 'Vendor or Sweet not found'}
            return make_response(jsonify(response), 404)

class DeleteVendorSweetResource(Resource):
    def delete(self, vendor_sweet_id):
        vendor_sweet = VendorSweet.query.get(vendor_sweet_id)
        if vendor_sweet:  # Check if vendor_sweet is found
            db.session.delete(vendor_sweet)
            db.session.commit()
            return {}, 204
        else:
            return {"error": "VendorSweet not found"}, 404


api.add_resource(VendorsResource, '/vendors')
api.add_resource(VendorResource, '/vendors/<int:vendor_id>')
api.add_resource(SweetsResource, '/sweets')
api.add_resource(SweetResource, '/sweets/<int:sweet_id>')
api.add_resource(VendorSweetResource, '/vendor_sweets')
api.add_resource(DeleteVendorSweetResource, '/vendor_sweets/<int:vendor_sweet_id>')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


