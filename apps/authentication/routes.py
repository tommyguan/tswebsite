# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import requests
import json
from datetime import datetime
from datetime import date
from flask_restx import Resource, Api
from flask_login import login_required
from apps.api.spy import *  # Import the utils module
from apps.api import ib
import flask
import finnhub
import asyncio
from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from flask_dance.contrib.github import github

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, EditUserAssetForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass, generate_token

# Bind API -> Auth BP
api = Api(blueprint)

server='52.52.192.236'
#server = 'localhost'

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/updateuser')
def updateuser():
    url = "https://" + server + "/api/users/"

    payload = {}
    headers = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload, verify=False)

    print(response.text)
    return render_template('accounts/list.html', users=response.json()['data'])
# Login & Registration


@blueprint.route("/github")
def login_github():
    """ Github login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    res = github.get("/user")
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if flask.request.method == 'POST':

        # read form data
        username = request.form['username']
        password = request.form['password']

        # return 'Login: ' + username + ' / ' + password

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    else:
        return render_template('accounts/login.html',
                               form=login_form)

@blueprint.route('/trade/account_balance', methods=['GET', 'POST'])
#@login_required
def account_balance():
    if(ib is None):
        return {
            'message': 'Fail to connect to IB !!!',
            'success': False
        }, 500
    else:
        cash, buying_power, net_asset = portfolio_balance(ib,'U2120530')
        return {
            'cash': cash,
            'buying_power': buying_power,
            'net_asset': net_asset,
            'success': True
        }, 200

@blueprint.route('/trade/portfolio_spy', methods=['GET', 'POST'])
#@login_required
def current_portfolio_spy():
    if(ib is None):
        return {
            'message': 'Fail to connect to IB !!!',
            'success': False
        }, 500
    else:
        spy_position, call_amt, put_amt, positions_to_roll = portfolio_spy(ib,'U2120530')
        return {
            'spy_position': spy_position,
            'call_amt': call_amt,
            'put_amt': put_amt,
            'positions_to_roll': positions_to_roll,
            'success': True
        }, 200
    
@blueprint.route('/trade/open_orders', methods=['GET', 'POST'])
#@login_required
def open_orders():
    if(ib is None):
        return {
            'message': 'Fail to connect to IB !!!',
            'success': False
        }, 500
    else:
        open_orders = open_trades(ib)
        #trade_dicts = [util.tree(trade) for trade in open_orders]

        # Convert trade dictionaries to JSON format
        #trade_json = json.dumps(trade_dicts, default=str, indent=4)
        return {
            'trades': "trade_json",
            'success': True
        }, 200

@blueprint.route('/trade/price', methods=['GET', 'POST'])
#@login_required
def price():
    if(ib is None):
        return {
            'message': 'Fail to connect to IB !!!',
            'success': False
        }, 500
    else:
        FINN_KEY = 'cnn6ls9r01qq36n5qi6gcnn6ls9r01qq36n5qi70'
        finnhub_client = finnhub.Client(api_key=FINN_KEY)

        symbol = 'SPY'
        current_price = finnhub_client.quote(symbol)['c']
        strike_price = math.ceil(current_price)
        return {
            'symbol': symbol,
            'price': current_price,
            'strike_price': strike_price,
            'success': True
        }, 200
    
@blueprint.route('/spy_trade', methods=['GET', 'POST'])
#@login_required
def spy_trade():
    return render_template('home/spy-trade.html')

@blueprint.route('/balance', methods=['GET', 'POST'])
#@login_required
def balance():
    edit_asset_form = EditUserAssetForm(request.form)

    # get current users information
    url = "https://"+server+"/api/users/"
    #get total information
    total_url = "https://"+server+"/api/users/0"

    headers = {}

    payload = {}

    response = requests.request("GET", url, headers=headers, verify=False)

    if 'balance' in request.form:

        balance = float(request.form['balance'])

        for user in response.json()['data']:
            update_url = "https://"+server+"/api/users/" + str(user['id'])

            payload = {'current_balance': round(
                balance * user['interest_rate'], 2), 'change': round((round(
                    balance * user['interest_rate'], 2)-float(user['total_invest']))/float(user['total_invest'])*100, 2), 'balance_update_date': date.today()}
            files = [

            ]
            
            response = requests.request(
                "PUT", update_url, headers=headers, data=payload, files=files, verify=False)
            
        #validate total balance of each user add up is the total balance of company account
        total = requests.request("GET", total_url, headers=headers, verify=False).json()['data']
        gap = abs(float(total[0]['total_balance']) - balance)
        if(gap > 10):
            return 'There is problem. The balance of each user addup has a big gap with the company total balance, Please contact SUPPORT ASAP. The GAP is ' + str(gap)

        return render_template('accounts/edit_assets.html', form=edit_asset_form, users=requests.request("GET", url, headers=headers, data=payload, verify=False).json()['data'],total=total)

    else:

        return render_template('accounts/edit_assets.html', form=edit_asset_form, users=requests.request("GET", url, headers=headers, verify=False).json()['data'],total=requests.request("GET", total_url, headers=headers, data=payload, verify=False).json()['data'])


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@api.route('/login/jwt/', methods=['POST'])
class JWTLogin(Resource):
    def post(self):
        try:
            data = request.form

            if not data:
                data = request.json

            if not data:
                return {
                    'message': 'username or password is missing',
                    "data": None,
                    'success': False
                }, 400
            # validate input
            user = Users.query.filter_by(username=data.get('username')).first()
            if user and verify_pass(data.get('password'), user.password):
                try:

                    # Empty or null Token
                    if not user.api_token or user.api_token == '':
                        user.api_token = generate_token(user.id)
                        user.api_token_ts = int(datetime.utcnow().timestamp())
                        db.session.commit()

                    # token should expire after 24 hrs
                    return {
                        "message": "Successfully fetched auth token",
                        "success": True,
                        "data": user.api_token
                    }
                except Exception as e:
                    return {
                        "error": "Something went wrong",
                        "success": False,
                        "message": str(e)
                    }, 500
            return {
                'message': 'username or password is wrong',
                'success': False
            }, 403
        except Exception as e:
            return {
                "error": "Something went wrong",
                "success": False,
                "message": str(e)
            }, 500


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

# Errors


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
