#!/usr/bin/env python

from ib_insync import *
import requests
import math
import pandas as pd
from pandas_market_calendars import get_calendar
from datetime import datetime


def spread_order(ib, amt,  long_strike, long_exp,  short_strike, short_exp, right, account):
    
    long_option = Option('SPY', long_exp, long_strike, right, exchange='SMART', multiplier='100')
    short_option = Option('SPY', short_exp, short_strike, right, exchange='SMART', multiplier='100') 

    ib.qualifyContracts(short_option,long_option)
    
    combo_Legs = [ComboLeg(conId=short_option.conId,ratio=1, action='SELL',exchange='SMART'),ComboLeg(conId=long_option.conId,ratio=1, action='BUY',exchange='SMART')  ]


##nbbo price

    short_ticker = ib.reqTickers(short_option)[0]
    long_ticker = ib.reqTickers(long_option)[0]
    
    short_mid = (short_ticker.bid + short_ticker.ask) / 2
    long_mid = (long_ticker.bid + long_ticker.ask) / 2
    limit_price = long_mid - short_mid
    
    
    combo = Bag(symbol='SPY', comboLegs=combo_Legs,exchange='SMART', currency='USD')
    
    trade =ib.placeOrder(combo,LimitOrder("BUY", amt, limit_price), account=account)
    
    print(trade)
    trade.isDone()  # Wait for the order to be filled

 

def rollout(ib, position_to_roll, short_strike, short_exp, right, account):
    
    long_option = position_to_roll.contract
    amt = -(position_to_roll.position)
    short_option = Option('SPY', short_exp, short_strike, right, exchange='SMART', multiplier='100') 

    ib.qualifyContracts(short_option,long_option)

    ##nbbo price

    short_ticker = ib.reqTickers(short_option)[0]
    long_ticker = ib.reqTickers(long_option)[0]

    short_mid = (short_ticker.bid + short_ticker.ask) / 2
    long_mid = (long_ticker.bid + long_ticker.ask) / 2
    limit_price = long_mid - short_mid
    
    combo_Legs = [ComboLeg(conId=short_option.conId,ratio=1, action='SELL',exchange='SMART'),ComboLeg(conId=long_option.conId,ratio=1, action='BUY',exchange='SMART')]
   
    combo = Bag(symbol='SPY', comboLegs=combo_Legs,exchange='SMART', currency='USD')

    if not if_order_exists(ib, combo):
        trade =ib.placeOrder(combo,LimitOrder("BUY", amt, limit_price), account)
        print(trade)
        #trade.isDone()  # Wait for the order to be filled

def if_order_exists(ib, contract):

    existing_orders = ib.orders()
    openTrades = ib.openTrades()
    
    order_already_placed = False

    for trade in openTrades:
        if trade.contract == contract:
            order_already_placed = True
            break

    return order_already_placed



def sell_option (ib, amt, exp, strike_price, right, account):
  
    contract = Option('SPY', exp, strike_price, right, 'SMART', multiplier='100')


# Request market data for the SPY put option
    ib.qualifyContracts(contract)
    ticker = ib.reqTickers(contract)[0]

# Calculate the midpoint between the bid and ask prices
    limit_price = (ticker.bid + ticker.ask) / 2
    
# Place a limit order to sell the SPY put option at the midpoint price
    order = LimitOrder('SELL', amt, limit_price)

# Place the order
    trade = ib.placeOrder(contract, order, account)


    print("Trade:", trade)

# Wait for the order to fill
    #trade.isDone()  # Wait for the order to be filled
    print(f"Order Status: {trade.orderStatus}")
    
   # ib.disconnect()

def get_quote (ib, symbol):
    contract = Stock(symbol, 'SMART', 'USD')

    ib.qualifyContracts(contract)

    ticker = ib.reqTickers(contract)[0]
    value = ticker.marketPrice()
    return value


def get_date ():    
    today_date = datetime.today().strftime('%Y%m%d')
    # Create a market calendar for the NYSE (New York Stock Exchange)
    nyse = get_calendar('XNYS')
    # Get the next trading day
    next_trading_day = nyse.valid_days(start_date=datetime.today(), end_date=datetime.today() + pd.Timedelta(days=10))[1].strftime('%Y%m%d')
    
    # Get today's date
    # Print today's date in the desired format
    print("Today's date in YYYYMMDD format:", today_date)
    print("Next trading day after", today_date, "is:", next_trading_day)
    return today_date, next_trading_day



def portfolio_balance (ib, account):
    account_values = ib.accountValues(account)    

    cash = buying_power = net_asset = 0

    for item in account_values:
        if item.tag == 'CashBalance':
            cash = float(item.value)
        elif item.tag == 'BuyingPower':
            buying_power = float(item.value)
        elif item.tag == 'NetLiquidationByCurrency':
            net_asset = float(item.value)
    print("cash:", cash, "buying_power:", buying_power, "net_asset:", net_asset)
    return cash, buying_power, net_asset   

def open_trades(ib):
    
    open_orders = ib.reqAllOpenOrders()
    
    return open_orders

def get_beta(symbol):
    stock_contract = Stock(symbol, 'SMART', 'USD')  # Replace 'AAPL' with the desired stock symbol
    beta = None
    ib.qualifyContracts(stock_contract)
    fundamental_data = ib.reqFundamentalData(stock_contract, 'ReportSnapshot')

    for field in fundamental_data:
        print(field)
        '''
        if field.name == 'beta':
            beta = field.value
            print(f"Beta for {stock_contract.symbol}: {beta}")
            break
            '''
    else:
        print(f"Beta not found for {stock_contract.symbol}")
    
    return beta


def portfolio_spy (ib,account):
    spy_position = call_amt = put_amt = 0
    positions_to_roll = []
    weighted_delta = weighted_theta = 0
    
    positions = ib.positions(account)
    for p in positions:
        if p.contract.secType == 'STK' and p.contract.symbol == 'SPY':
            spy_position = p.position /100
            weighted_delta += p.position
            
        if p.contract.secType == 'OPT' and p.contract.symbol == 'SPY':
            print("\t".join([p.contract.right, p.contract.lastTradeDateOrContractMonth, str(p.contract.strike), str(p.position)]))
            #ticker =  ib.reqTickers(p.contract)
            #print(ticker)
            
            #weighted_delta += ticker[0].modelGreeks.delta * p.position
            #weighted_theta += ticker[0].modelGreeks.theta * p.position
            
            positions_to_roll.append(p)

            if p.contract.right == 'C':
                call_amt = +p.position

                
            if p.contract.right == 'P':
                put_amt = +p.position

    print("SPY shares(x100):", spy_position, "calls:", call_amt, "puts:", put_amt)
    #print("SPY shares(x100):", spy_position, "calls:", call_amt, "puts:", put_amt, "delta:", weighted_delta, "theta:", weighted_theta)
    return (spy_position, call_amt, put_amt, positions_to_roll)




def do_at_open(account):


    current_date = datetime.now()
    print(current_date)
    today_date = current_date.strftime('%Y%m%d')

    print("Today's date in YYYYMMDD format:", today_date)
    # Create a market calendar for the NYSE (New York Stock Exchange)

    nyse = get_calendar('XNYS')
    is_trading_day = nyse.valid_days(start_date=today_date, end_date=today_date).size > 0

    ###change ip and port: tws paper: 7497 real: 7496
    if is_trading_day:
        FINN_KEY = 'cnn6ls9r01qq36n5qi6gcnn6ls9r01qq36n5qi70'
        finnhub_client = finnhub.Client(api_key=FINN_KEY)
        
        util.startLoop()
        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=88)

        accounts = ib.managedAccounts()

        # Print the list of accounts
        #print("Accounts under management:")
        for account in accounts:
            cash, buying_power, net_asset = portfolio_balance(ib, account)
            spy_position, call_amt, put_amt, positions_to_roll = portfolio_spy(ib, account)

            ##### sell CC if cc_amt > 0
        
            symbol = 'SPY'
            #current_price = finnhub_client.quote(symbol)['c']
            current_price = get_quote(ib, symbol)


            strike_price = math.ceil(current_price)
            cc_amt = 5 if spy_position + call_amt > 5 else spy_position + call_amt

            if cc_amt > 0:
                sell_option(ib, cc_amt, today_date, strike_price, 'C', account)

                ##### sell puts:
                max_position = int(net_asset * 2.5 / current_price / 100)
                if put_amt == 0 :

                    short_put_amt = 5 if max_position - spy_position > 5 else max_position - spy_position
                    sell_option(ib, short_put_amt, today_date, strike_price, 'P', account)

        ib.disconnect()

    else:
        print("Today is not a trading day.")

    


def do_at_close(account):
    current_date = datetime.now()
    print(current_date)
    today_date = current_date.strftime('%Y%m%d')
    print("Today's date in YYYYMMDD format:", today_date)
    # Create a market calendar for the NYSE (New York Stock Exchange)
    
    nyse = get_calendar('XNYS')
    is_trading_day = nyse.valid_days(start_date=today_date, end_date=today_date).size > 0


    if is_trading_day:
    
        next_trading_day = nyse.valid_days(start_date=datetime.today(), end_date=datetime.today() + pd.Timedelta(days=10))[1].strftime('%Y%m%d')
        print("Next trading day after", today_date, "is:", next_trading_day)

        FINN_KEY = 'cnn6ls9r01qq36n5qi6gcnn6ls9r01qq36n5qi70'
        finnhub_client = finnhub.Client(api_key=FINN_KEY)

        symbol = 'SPY'
        current_price = finnhub_client.quote(symbol)['c']
        print("current price: ", current_price)

        
        ###change ip and port: tws paper: 7497 real: 7496
        util.startLoop()
        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=88)

        for account in accounts:
            cash, buying_power, net_asset = portfolio_balance(ib, account)
            spy_position, call_amt, put_amt, positions_to_roll = portfolio_spy(ib, account)

            for p in positions_to_roll:
                if p.contract.lastTradeDateOrContractMonth == today_date:
                    #print("position to roll:", p)
                    if abs(p.contract.strike - current_price) <= 3:
                        rollout(ib, p, p.contract.strike, next_trading_day, p.contract.right, account)

        ib.disconnect()

    else:
        print("Today is not a trading day.")






    





