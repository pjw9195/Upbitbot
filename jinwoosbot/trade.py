from key import *
import pyupbit
import websocket
import time
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time
access_key = ac_key
secret_key = se_key
upbit = pyupbit.Upbit(access_key, secret_key)

def mybalnace():
    # 내 돈
    print(upbit.get_balances())
    # print((upbit.get_balances())[0][0]['currency'] +' : ' + (upbit.get_balances())[0][0]['balance'] )

def find():
    def on_message(ws, message):
        get_message = json.loads(message.decode('utf-8'))
        print(get_message)
        global msg_ask
        msg_ask = get_message['orderbook_units'][5]['ask_price']
        global msg_bid
        msg_bid = get_message['orderbook_units'][3]['bid_price']
        global msg_cur
        msg_cur = get_message['orderbook_units'][0]['bid_price']
        # 한번만받고 종료.
        ws.close()


    def on_error(ws, error):
        print(error)

    def on_close(ws):
        print("close")


    def on_open(ws):
        def run(*args):
            ws.send('[{"ticket":"test"},{"type":"orderbook","codes":["KRW-BTC"]}]')

            time.sleep(0.1)

        thread.start_new_thread(run, ())

    ws = websocket.WebSocketApp("wss://api.upbit.com/websocket/v1",
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)

    ws.on_open = on_open
    ws.run_forever()

def buy():
    find()
    getbalance = upbit.get_balances()
    KRW = getbalance[0][0]['balance']
    num = (float(KRW)*0.9/float(msg_ask))
    ret = upbit.buy_limit_order("KRW-BTC", msg_ask, num )
    print(ret)
    cur = msg_cur
    while True:
        find()
        if cur*0.95 > msg_cur:
            sell()
            break
        elif cur*1.05 <msg_cur:
            sell()
            break
        time.sleep(1)


def sell():
    find()
    ret = upbit.sell_limit_order("KRW-BTC", msg_bid, (upbit.get_balances())[0][0]['balance'])
    print(ret)