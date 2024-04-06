import json
from spy_live import *  # Import the utils module
from ib_insync import *
from global_vars import *

ib = IB()

ib.connect(tws_ip, 7497, clientId=8, timeout=300)

# Request open orders
open_orders = ib.reqAllOpenOrders()
# for order in open_orders:
order1 = '{\"key\":\"value\"}'
order2 = '{\"key\":\"value\"}'
print(order1 + '\n' + order2)
orders = ''
order_no = 0
for order in open_orders:
    order_no = order_no + 1
    order = '{\"conId\":\"{}\",\"key\":\"{}\"}'.format(order.contract.conId,order.contract.conId)
    if order_no > 1:
        order = '\n' + order
    orders = orders + order

ib.disconnect()
print(orders)

