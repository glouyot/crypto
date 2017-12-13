from bittrex import Bittrex, API_V2_0
import time
import json

walets = None
total = 0

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

def print_total(total):
    print('Total\t: ' + str(total))
    
def print_balances(walets):
    global total
    total = 0
    data = walets.get_balances()
    for cu in data['result']:
        if cu['Balance']['Balance'] > 0:
            if cu['Balance']['Currency'] == 'BTC':
                total += cu['Balance']['Balance']
                print(cu['Balance']['Currency'] + '\t: ' + str(cu['Balance']['Balance']))
            else:
                total += cu['Balance']['Balance'] * cu['BitcoinMarket']['Last']
                print(cu['Balance']['Currency'] + '\t: ' + str(cu['Balance']['Balance']) + '\t\tLast : ' + str(cu['BitcoinMarket']['Last']) + '\t\tBid : ' + str(cu['BitcoinMarket']['Bid']) + '\t\tAsk : ' + str(cu['BitcoinMarket']['Ask']))

if __name__ == '__main__':
    walets = create()   
    while True:
        print('-------------------------------------------------------------')
        print_balances(walets)
        print_total(total)
        time.sleep(5)
