from . import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates

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
