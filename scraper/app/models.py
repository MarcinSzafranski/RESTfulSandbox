"""
Module for ORM models, structure of the database.
"""
from app import db


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(200))
    images = db.relationship('Image', backref=db.backref('url'))
    textcontent = db.relationship('TextContent', backref=db.backref('url'))


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))


class TextContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
