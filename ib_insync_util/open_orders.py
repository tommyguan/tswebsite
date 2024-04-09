import json
from spy_live import *  # Import the utils module
from ib_insync import *
from global_vars import *

ib = IB()

ib.connect(tws_ip, 7497, clientId=8, timeout=300)

# Request open orders
open_orders = ib.reqAllOpenOrders()
# for order in open_orders:
orders = ''
order_no = 0
for open_order in open_orders:
    order_no = order_no + 1
    order = ("{\"conId\":\"" + str(open_order.contract.conId) + "\"" + "," 
    + "\"time\":\"" + str(open_order.log[0].time) + "\"" + ","
    + "\"symbol\":\"" + open_order.contract.symbol + "\"" + ","
    + "\"right\":\"" + open_order.contract.right + "\"" + ","
    + "\"action\":\"" + open_order.order.action + "\"" + ","
    + "\"totalQuantity\":\"" + str(open_order.order.totalQuantity) + "\"" + ","
    + "\"orderType\":\"" + open_order.order.orderType + "\"" + ","
    + "\"lmtPrice\":\"" + str(open_order.order.lmtPrice) + "\"" + ","
    + "\"account\":\"" + open_order.order.account + "\"" + ","
    + "\"status\":\"" + open_order.orderStatus.status + "\"" + ","
    + "\"filled\":\"" + str(open_order.orderStatus.filled) + "\"" + ","
    + "\"remaining\":\"" + str(open_order.orderStatus.remaining) + "\"" + ","
    + "\"avgFillPrice\":\"" + str(open_order.orderStatus.avgFillPrice) + "\"" 
    + "}" )
    if order_no > 1:
        order = '\n' + order
    orders = orders + order

ib.disconnect()
print(orders)

