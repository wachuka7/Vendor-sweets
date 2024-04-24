from . import db
from sqlalchemy_serializer import SerializerMixin


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
