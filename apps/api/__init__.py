# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

from ib_insync import *

ib = IB()
try:
    ib.connect('54.151.16.77', 7497, clientId=998)
    print('Success to connect to IB !!!!')
    #IB.run()

except:
    print('Fail to connect to IB !!!!')

blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix='/api'
)
