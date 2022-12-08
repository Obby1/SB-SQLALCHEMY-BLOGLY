"""Seed file to make sample data for db"""
# python seed.py

from models import db, first_name, last_name, image_url
from app import app

#Create all tables
db.drop_all()
db.create_all()


