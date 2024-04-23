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
    name = db.Column(db.String, nullable=False)
    #Relationship
    vendor_sweets = db.relationship('VendorSweet', back_populates='sweet', cascade="all, delete")
    #Serialization
    def serialize(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f'<Sweet id={self.id} name={self.name}>'

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #Relationship
    vendor_sweets = db.relationship('VendorSweet', back_populates='vendor', cascade="all, delete")
    #Serialization
    def serialize(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f'<Vendor id={self.id} name={self.name}>'  
    
class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)

   #Relationship
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')
    vendor = db.relationship('Vendor', back_populates='vendor_sweets')

    #Serialization
    def serialize(self):
        return {"id": self.id, "price": self.price, "vendor_id": self.vendor_id, "sweet_id": self.sweet_id}

    #Validation
    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError('Price must have a value')
        if price < 0:
            raise ValueError("Price must not be a negative value")
        return price 

    def __repr__(self):
         return f'<VendorSweet id={self.id} price={self.price}, vendor_id={self.vendor_id} sweet_id={self.sweet_id}>'