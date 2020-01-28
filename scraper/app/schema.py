"""
Module for ORM models schemas, used to serialize/deserialize data.
"""
from app.models import Url, Image, TextContent
from app import ma


class UrlSchema(ma.ModelSchema):
    class Meta:
        model = Url


class ImageSchema(ma.ModelSchema):
    class Meta:
        model = Image


class TextContentSchema(ma.ModelSchema):
    class Meta:
        model = TextContent
