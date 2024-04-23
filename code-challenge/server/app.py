from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
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
api = Api(app)

db.init_app(app)

class Home(Resource):
    def get(self):
        return '<h1>Code challenge</h1>'

api.add_resource(Home, "/")

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    serialized_vendors = [{"id": vendor.id, "name": vendor.name} for vendor in vendors]
    return make_response(jsonify(serialized_vendors), 200)

@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = db.session.get(Vendor, id)
    if vendor is None:
        return jsonify({"error": "Vendor not found"}), 404
    serialized_vendor = {
        "id": vendor.id,
        "name": vendor.name,
        "vendor_sweets": [vs.serialize() for vs in vendor.vendor_sweets]
    }
    return jsonify(serialized_vendor), 200


@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    serialized_sweets = [{"id": sweet.id, "name": sweet.name} for sweet in sweets]
    return make_response(jsonify(serialized_sweets), 200)

@app.route('/sweets/<int:id>', methods=['GET'])
def get_sweet(id):
    sweet = db.session.get(Sweet, id)
    if sweet is None:
        return jsonify({"error": "Sweet not found"}), 404
    serialized_sweet = sweet.serialize()
    return make_response(jsonify(serialized_sweet), 200)

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')

    # To validate the input
    if price is None or price < 0 or not vendor_id or not sweet_id:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    # Create the new VendorSweet instance
    new_vs = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
    db.session.add(new_vs)
    db.session.commit() 

    # Expected new VendorSweet details
    serialized_vendor_sweet = {
        "id": new_vs.id,
        "price": new_vs.price,
        "sweet": new_vs.sweet.serialize(),
        "sweet_id": sweet_id,
        "vendor": new_vs.vendor.serialize(),
        "vendor_id": vendor_id
    }
    return make_response(jsonify(serialized_vendor_sweet), 201)

@app.route('/vendor_sweets/<int:id>', methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = db.session.get(VendorSweet, id)
    if vendor_sweet is None:
        return jsonify({"error": "VendorSweet not found"}), 404
    db.session.delete(vendor_sweet)
    db.session.commit()
    return make_response(jsonify({}), 204)

if __name__ == '__main__':
    app.run(port=5555, host='127.0.0.1', debug=True)