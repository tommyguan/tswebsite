import json
from spy_live import *  # Import the utils module
from ib_insync import *
from global_vars import *

ib = IB()

ib.connect(tws_ip, 7497, clientId=8, timeout=300)

# Request open orders
open_orders = ib.reqAllOpenOrders()
# for order in open_orders:
for order in open_orders:
    print('{conId:'+order.contract.conId+'}')

# trade_dicts = [util.tree(trade) for trade in open_orders]

# Convert trade dictionaries to JSON format
# trade_json = json.dumps(trade_dicts, default=str, indent=4)

# Print or save the JSON string
# print(open_orders)
ib.disconnect()
