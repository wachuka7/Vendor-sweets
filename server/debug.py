#!/usr/bin/env python3

from app import app
from models import db
from models.sweet import Sweet
from models.vendor import Vendor
from models.vendor_sweet import  VendorSweet

if __name__ == '__main__':
    with app.app_context():
        import ipdb; ipdb.set_trace()