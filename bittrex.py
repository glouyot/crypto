from bittrex import Bittrex, API_V2_0
import time
import json

walets = None
total = 0
last_usdt = 0

def create():
    keys = open('key.json')
    data = json.load(keys)
    for cu in data:
        if cu == 'key':
            api_key = data[cu]
        if cu == 'secret':
            secret_key = data[cu]
    if api_key and secret_key:
        walets = Bittrex(api_key, secret_key, api_version=API_V2_0) 
    else:
        walets = Bittrex(None, None, api_version=API_V2_0)
    keys.close()
    return(walets)

def print_total(total, last_usdt):
    print('Total\t: ' + str(total) + '\tUSDT : ' + str(last_usdt * total))

def print_last_orders(walets):
    data = walets.get_order_history()
    for cu in data:
        print data[cu]
    
def print_info(walets):
    data = walets.get_balances()
    for cu in data['result']:
        if cu['Balance']['Balance'] > 0:
            print cu

def order_book_sum(walets, market_name, scale=10):
    data = walets.get_orderbook(market_name)
    buy_data = data['result']['buy']
    sell_data =data['result']['sell']
    buy = 0
    sell = 0
    for i in range(scale):
        buy += data['result']['buy'][i]['Rate'] * data['result']['buy'][i]['Quantity']
        sell += data['result']['sell'][i]['Rate'] * data['result']['sell'][i]['Quantity']
    ret = {'Buy': buy, 'Sell': sell}
    return(ret)

def print_balances(walets):
    global total
    total = 0
    global last_usdt
    data = walets.get_balances()
    for cu in data['result']:
        if cu['Balance']['Balance'] > 0:
            if cu['Balance']['Currency'] == 'BTC':
                total += cu['Balance']['Balance']
                print(cu['Balance']['Currency'] + '\t: ' + str(cu['Balance']['Balance']))
            else:
                if cu['BitcoinMarket'] is not None:
                    total += cu['Balance']['Balance'] * cu['BitcoinMarket']['Last']
                    print(cu['Balance']['Currency'] + '\t: ' + str(cu['Balance']['Balance']) + '\t\tLast : ' + str(cu['BitcoinMarket']['Last']) + '\t\tBid : ' + str(cu['BitcoinMarket']['Bid']) + '\t\tAsk : ' + str(cu['BitcoinMarket']['Ask']))
                elif cu['FiatMarket'] is not None:
                    last_usdt = cu['FiatMarket']['Last']
                    print(cu['Balance']['Currency'] + '\t: ' + str(cu['Balance']['Balance']) + '\t\tLast : ' + str(cu['FiatMarket']['Last']) + '\t\tBid : ' + str(cu['FiatMarket']['Bid']) + '\t\tAsk : ' + str(cu['FiatMarket']['Ask']))
 
if __name__ == '__main__':
    walets = create()   
    #print_info(walets)
"""    while True:
        time.sleep(5)
        print_balances(walets)
        print_total(total, last_usdt)
        print('--------------------------------------------------------')"""
#    print_last_orders(walets)
#https://bittrex.com/api/v2.0/pub/market/GetLatestTick?marketname=BTC-LTC&tickInterval=fivemin
