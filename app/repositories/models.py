from datetime import datetime

from app.plugins import db


class Order(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(80))
    client_dni = db.Column(db.String(10))
    client_address = db.Column(db.String(128))
    client_phone = db.Column(db.String(15))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float)
    size_id = db.Column(db.Integer, db.ForeignKey("size._id"))
    size = db.relationship("Size", backref=db.backref("size"))
    detail = db.relationship("OrderDetail", backref=db.backref("order_detail"))


class Element(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    element_type = db.Column(db.String(20))
    __mapper_args__ = {
        "polymorphic_identity": "element",
        "polymorphic_on": element_type,
    }


class Ingredient(Element):
    __mapper_args__ = {"polymorphic_identity": "ingredient"}


class Beverage(Element):
    __mapper_args__ = {"polymorphic_identity": "beverage"}


class Size(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)


class OrderDetail(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order._id"))
    element_id = db.Column(db.Integer, db.ForeignKey("element._id"))
    element = db.relationship("Element", backref=db.backref("element"))
    element_price = db.Column(db.Float)
