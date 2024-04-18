from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
 

# import os

# from flask import Flask, request, jsonify, make_response
# from flask_migrate import Migrate
# from flask_restful import Resource, Api

# from models import db, Sweet, Vendor, VendorSweet
# from dotenv import load_dotenv
# load_dotenv()
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get(
#     "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)

# db.init_app(app)
# api = Api(app)

# @app.route('/')
# def home():
#     return '<h1>Code challenge</h1>'

# # getting all vendors
# class VendorsResource(Resource):
#     def get(self):
#         vendors = Vendor.query.all()
#         vendors_data = [{'id': vendor.id, 'name': vendor.name} for vendor in vendors]
#         return jsonify(vendors_data)


# # getting vendor by ID
# class VendorResource(Resource):
#     def get(self, vendor_id):
#         vendor = Vendor.query.get(vendor_id)
#         if vendor:
#             vendor_data = {
#                 'id': vendor.id,
#                 'name': vendor.name,
#                 'vendor_sweets': [
#                     {
#                         'id': vendor_sweet.id,
#                         'price': vendor_sweet.price,
#                         'sweet': {'id': vendor_sweet.sweet.id, 'name': vendor_sweet.sweet.name},
#                         'sweet_id': vendor_sweet.sweet_id,
#                         'vendor_id': vendor_sweet.vendor_id
#                     } for vendor_sweet in vendor.vendor_sweets]
#             }
#             return jsonify(vendor_data)
#         else:
#             response = {'error': 'Vendor not found'}
#             response = make_response(jsonify(response), 404)
#             return response


# # getting all sweets
# class SweetsResource(Resource):
#     def get(self):
#         sweets = Sweet.query.all()
#         sweets_data = [{'id': sweet.id, 'name': sweet.name} for sweet in sweets]
#         return jsonify(sweets_data)


# # getting specific sweet by ID
# class SweetResource(Resource):
#     def get(self, sweet_id):
#         sweet = Sweet.query.get(sweet_id)
#         if sweet:
#             sweet_data = {'id': sweet.id, 'name': sweet.name}
#             return jsonify(sweet_data)
#         else:
#             response = {'error': 'Sweet not found'}
#             response = make_response(jsonify(response), 404)
#             return response


# class VendorSweetResource(Resource):
#     def post(self):
#         data = request.get_json()
#         price = data.get('price')
#         vendor_id = data.get('vendor_id')
#         sweet_id = data.get('sweet_id')

#         errors = []

#         if None in (price, vendor_id, sweet_id):
#             errors.append('price, vendor_id, and sweet_id are required')

#         # Validating price to ensure it's non-negative
#         if price < 0:
#             errors.append('Price must be non-negative.')

#         if errors:
#             response = jsonify({'errors': ['validation errors']})
#             return make_response(response, 400)

#         vendor = Vendor.query.get(vendor_id)
#         sweet = Sweet.query.get(sweet_id)

#         new_vendor_sweet = VendorSweet(price=price, vendor=vendor, sweet=sweet)
#         db.session.add(new_vendor_sweet)

#         try:
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             response = jsonify({'errors': str(e)})
#             return make_response(response, 400)

#         vendor_sweet_data = {
#             'id': new_vendor_sweet.id,
#             'price': new_vendor_sweet.price,
#             'sweet': {'id': sweet.id, 'name': sweet.name},
#             'sweet_id': sweet.id,
#             'vendor': {'id': vendor.id, 'name': vendor.name},
#             'vendor_id': vendor.id
#         }

#         response = jsonify(vendor_sweet_data)
#         return make_response(response, 201)


# class DeleteVendorSweetResource(Resource):
#     def delete(self, vendor_sweet_id):
#         vendor_sweet = VendorSweet.query.get(vendor_sweet_id)
#         if vendor_sweet:
#             db.session.delete(vendor_sweet)
#             db.session.commit()
#             return {}, 204
#         else:
#             return {'error': 'VendorSweet not found'}, 404


# api.add_resource(VendorsResource, '/vendors')
# api.add_resource(VendorResource, '/vendors/<int:vendor_id>')
# api.add_resource(SweetsResource, '/sweets')
# api.add_resource(SweetResource, '/sweets/<int:sweet_id>')
# api.add_resource(VendorSweetResource, '/vendor_sweets')
# api.add_resource(DeleteVendorSweetResource, '/vendor_sweets/<int:vendor_sweet_id>')

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendor_sweets = db.relationship('VendorSweet', back_populates='sweets', cascade='all, delete-orphan')
    vendors = db.relationship('Vendor', secondary='vendor_sweets', back_populates='sweets')
    
    # Add serialization
    serialize_rules=['-vendor_sweets.sweet']
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    sweets = db.relationship('Sweet', secondary='vendor_sweets', back_populates='vendors')
    vendor_sweets = db.relationship('VendorSweet', back_populates='vendors', cascade='all, delete-orphan')
    # Add serialization
    serialize_rules=['-vendor_sweets.vendor']
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    vendor_id = db.Column(db.Integer, ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, ForeignKey('sweets.id'))

    # Add relationships
    vendors= db.relationship('Vendor', back_populates='vendor_sweets')
    sweets=db.relationship('Sweet', back_populates='vendor_sweets')
    # Add serialization
    serialize_rules = []
    # Add validation
    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError('Price cannot be none')
        elif price<0:
            raise ValueError('Price cannot be lower than zero')
        else:
            return price

    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
