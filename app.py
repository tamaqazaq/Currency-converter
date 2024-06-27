from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Ваш API ключ
API_KEY = '998a560e445ed322f603da18'
BASE_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest'

# Определим список валют с полными наименованиями
currencies = [
    {"code": "USD", "name": "United States Dollar"},
    {"code": "EUR", "name": "Euro"},
    {"code": "GBP", "name": "British Pound Sterling"},
    {"code": "JPY", "name": "Japanese Yen"},
    {"code": "AUD", "name": "Australian Dollar"},
    {"code": "CAD", "name": "Canadian Dollar"},
    {"code": "CHF", "name": "Swiss Franc"},
    {"code": "CNY", "name": "Chinese Yuan Renminbi"},
    {"code": "SEK", "name": "Swedish Krona"},
    {"code": "NZD", "name": "New Zealand Dollar"}
]

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount = float(request.form.get('amount'))
        
        response = requests.get(f'{BASE_URL}/{from_currency}')
        
        if response.status_code != 200:
            return f"Error: Unable to fetch data from API. Status code: {response.status_code}"
        
        data = response.json()
        
        if 'conversion_rates' not in data:
            return f"Error: 'conversion_rates' key not found in API response. Response: {data}"
        
        rates = data['conversion_rates']
        if to_currency not in rates:
            return f"Error: The currency ({to_currency}) is not found in the rates."

        to_rate = rates[to_currency]
        
        converted_amount = amount * to_rate
        return render_template('convert.html', currencies=currencies, converted_amount=converted_amount, to_currency=to_currency, from_currency=from_currency, amount=amount)
    
    return render_template('convert.html', currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)


