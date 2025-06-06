
from flask import Flask, request
import hmac, hashlib, time, requests
from urllib.parse import urlencode

app = Flask(__name__)

API_KEY = 'API_KEY_ANDA'
API_SECRET = 'API_SECRET_ANDA'

def indodax_order(pair, type_, price, amount):
    url = 'https://indodax.com/tapi'
    t = int(time.time())
    params = {
        'method': 'trade',
        'timestamp': t,
        'pair': pair,
        'type': type_,
        'price': price,
        'idr': amount
    }
    sign = hmac.new(API_SECRET.encode(), urlencode(params).encode(), hashlib.sha512).hexdigest()
    headers = {
        'Key': API_KEY,
        'Sign': sign
    }
    response = requests.post(url, data=params, headers=headers)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get('signal')
    price = float(data.get('price', 0))
    print(f"Received signal: {signal} at {price}")

    if signal == 'BUY':
        res = indodax_order('dogeusdt', 'buy', price, 500000)  # Entry Rp500.000
        print("BUY order executed:", res)
    elif signal == 'SELL':
        res = indodax_order('dogeusdt', 'sell', price, 500000)
        print("SELL order executed:", res)
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
