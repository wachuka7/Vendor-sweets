from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendor_sweets= db.relationship('VendorSweet', back_populates= 'sweets', cascade= 'all, delete-orphan')
    
    # Add serialization
    serialize_rules=['-vendor_sweets.sweets']
    
    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendor_sweets= db.relationship('VendorSweet', back_populates= 'vendors', cascade= 'all, delete-orphan')
    
    # Add serialization
    serialize_rules=['-vendor_sweets.vendors']
    
    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # Add relationships
    vendors= db.relationship('Vendor', back_populates='vendor_sweets')
    sweets=db.relationship('Sweet', back_populates='vendor_sweets')
    # Add serialization
    
    # Add validation
    @validates('price')
    def validate_price(self, key, price):
        if not price:
            raise ValueError('Price cannot be none')
        elif price<0:
            raise ValueError('Price cannot be lower than zero')
        else:
            return price

    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
