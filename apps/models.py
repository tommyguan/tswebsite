# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps import db

'''
Add your models below
'''

# Book Sample


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(100))

    oauth_github = db.Column(db.String(100), nullable=True)

    api_token = db.Column(db.String(100))
    api_token_ts = db.Column(db.Integer)
    current_balance = db.Column(db.Float)
    total_invest = db.Column(db.Integer)
    balance_update_date = db.Column(db.String(100))
    change = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
