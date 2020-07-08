"""
Example usage of Finnhub socket API.
"""

from __future__ import print_function # Py2 compat
import websocket
from finnhub_api.utils import get_finnhub_api_key


def write_line(data, fname):
    with open(fname, 'a+') as f:
        f.write(data + '\n')


def on_message(ws, message):
    write_line(message, tick_file)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    for symbol in SYMBOLS:
        subscribe(ws, symbol)


def subscribe(ws, symbol):
    template = '{"type":"subscribe","symbol":"X"}'
    req = template.replace('X', symbol.upper())
    ws.send(req)


tick_file = 'raw_ticks.txt'
token = get_finnhub_api_key()

SYMBOLS = [
    "AAPL",
    "SPY",
    "VXX",
    "BINANCE:ETHUSDT",
    "BINANCE:BTCUSDT"
]

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=" + token,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()