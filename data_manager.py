from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Postgres.sqlal import Currency, Admin, session
import asyncio
import decimal


app = Flask(__name__)


@app.route('/convert', methods=['GET'])
def convert_currency():
    currency_name = request.args.get('currency_name')
    amount = float(request.args.get('amount'))

    currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if not currency:
        return jsonify({'message': 'Валюта не найдена'}), 404

    else:
        convert_amount = f'{decimal.Decimal(amount) * decimal.Decimal(currency.rate)} RUB'
        session.close()
        return jsonify({'message': convert_amount}), 200


@app.route('/currencies', methods=['GET'])
def currencies():
    currencies = session.query(Currency).all()
    if currencies:
        currency_all = [{'name': currency.currency_name, 'rate': str(currency.rate) + ' RUB'} for currency in currencies]
        session.close()
        return jsonify({'message': currency_all}), 200
    else:
        response = "В базе данных не имеются сохраненные валюты"
        return jsonify({'message': response}), 400

if __name__ == "__main__":
    port = 5002
    app.run(debug=True, port = port)


    

