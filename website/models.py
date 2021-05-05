from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    productos = db.relationship('Producto')
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'))    

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    categoria = db.Column(db.String(255), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'))
    
    

class MiProducto(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Integer, default=0)
    descripcion = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    categoria = db.Column(db.String(255), default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    productos = db.relationship('Producto')
    usuarios = db.relationship('User')