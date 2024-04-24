# Code Challenge - API Documentation

## Introduction
This is a Sweet-Vendor project that implements a RESTful API for managing vendors, sweets, and their relationships. It provides endpoints for CRUD operations on vendors, sweets, and vendor sweets. This `README.md` gives the API documentation, outlines the available endpoints, their functionalities, and expected responses.

## Deployment
This API has been deployed and you can access it at [https://phase4-codechallenge-2.onrender.com/](https://phase4-codechallenge-2.onrender.com/).

## Setup
To set up the project:

1. Ensure you have Python 3 installed.
2. Clone the repository to your local machine.
```
git clone git@github.com:wachuka7/phase4-codechallenge-2.git
```
3. Navigate to the project directory.
4. Install the required dependencies using `pip install -r requirements.txt`.
5. Initialize the database by running `flask db init`.
6. Run database migrations using `flask db upgrade head`.
7. Seed the database with initial data by running `python server/seed.py`.
8. Start the Flask development server with `python app.py`.
9. The API will be accessible at `http://localhost:5000/`.

## Models
The API implements the following data models:

- Sweet: Represents a type of sweet.
- Vendor: Represents a vendor selling sweets.
- VendorSweet: Represents the relationship between vendors and sweets, including the price.

which are in sweet.py, vendor.py and vendor_sweet.py respectively.

## Validations
The API enforces the following validations:
- The price of a vendor sweet must be a non-negative integer.

## Routes
The API has the following routes:

### GET /vendors
Returns a list of all vendors.

### GET /vendors/<int:id>
Returns details of a specific vendor by ID.

### GET /sweets
Returns a list of all sweets.

### GET /sweets/<int:id>
Returns details of a specific sweet by ID.

### POST /vendor_sweets
Creates a new vendor sweet.

### DELETE /vendor_sweets/<int:id>
Deletes a vendor sweet by ID.

## Dependencies
The project relies on the following dependencies:
- Flask: Web framework for building the API.
- Flask-RESTful: Extension for creating RESTful APIs with Flask.
- Flask-Migrate: Extension for database migrations in Flask applications.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.

## Author
Rachael Wachuka
