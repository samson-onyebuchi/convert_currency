from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

url = os.getenv('EXCHANGE_RATES_URL')

@app.route('/convert_currency', methods=['POST'])
def convert_currency():
    try:
        base_currency = request.args.get('base_currency')
        target_currency = request.args.get('target_currency')
        amount = float(request.args.get('amount'))  # Convert amount to float

        if not url:
            raise ValueError("EXCHANGE_RATES_URL environment variable is not set.")

        response = requests.get(url)

        if response.status_code != 200:
            raise requests.RequestException(f"Failed to fetch exchange rates. Status code: {response.status_code}")

        exchange_rates = response.json().get('rates')

        if not exchange_rates:
            raise ValueError("No exchange rates data found.")

        if base_currency == 'USD':
            base_rate = 1.0
        else:
            base_rate = exchange_rates.get(base_currency)

        if target_currency == 'USD':
            target_rate = 1.0
        else:
            target_rate = exchange_rates.get(target_currency)

        if base_rate is None or target_rate is None:
            raise ValueError(f"Invalid currency: {base_currency}" if base_rate is None else f"Invalid currency: {target_currency}")

        converted_amount = amount * (target_rate / base_rate)
        result = {
            'base_currency': base_currency,
            'target_currency': target_currency,
            'amount': amount,
            'converted_amount': converted_amount
        }
        return jsonify(result)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400

    except requests.RequestException as re:
        return jsonify({'error': str(re)}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred.'}), 500

