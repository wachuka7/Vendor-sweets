from . import db
from sqlalchemy_serializer import SerializerMixin

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
    