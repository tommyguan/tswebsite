import json
from spy_live import *  # Import the utils module
from ib_insync import *
current_date = datetime.now()
print(current_date)
today_date = current_date.strftime('%Y%m%d')

print("Today's date in YYYYMMDD format:", today_date)
nyse = get_calendar('XNYS')
is_trading_day = nyse.valid_days(start_date=today_date, end_date=today_date).size > 0

if is_trading_day:

    next_trading_day = nyse.valid_days(start_date=datetime.today(), end_date=datetime.today() + pd.Timedelta(days=10))[1].strftime('%Y%m%d')
    print("Next trading day after", today_date, "is:", next_trading_day)

ib = IB()
ib.connect('54.151.16.77', 7497, clientId=2998,timeout=300)
trades = ib.trades()
for trade in trades:
    print(trade)
cash, buying_power, net_asset = portfolio_balance(ib,'U2120530')
print(cash)
# Request open orders
open_orders = ib.reqAllOpenOrders()
trade_dicts = [util.tree(trade) for trade in open_orders]

# Convert trade dictionaries to JSON format
trade_json = json.dumps(trade_dicts, default=str, indent=4)

# Print or save the JSON string
print(trade_json)
# Print details of each open order
