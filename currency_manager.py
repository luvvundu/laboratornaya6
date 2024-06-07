from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Postgres import  sqlal
from Postgres.sqlal import session, Currency, Admin
import asyncio
from aiohttp import web
from sqlalchemy import update

app = Flask(__name__)

@app.route('/load', methods=['POST'])
def load():
    data = request.get_json()
    currency_name = data.get('currency_name')
    rate = data.get('rate')
    if not currency_name or not rate:
        return jsonify({'message': 'Название валюты и курс являются обязательными для заполнения'}), 400

    new_currency = Currency(currency_name=currency_name, rate=rate)
    session.add(new_currency)
    session.commit()
    session.close()
    return jsonify({"message": "Валюта успешно добавлена"}), 200

@app.route('/update_currency', methods=['POST'])
def update_currency():
    data = request.get_json()
    currency_name = data["currency_name"]
    new_rate = data['new_rate']

    existing_currency = session.query(Currency).filter(Currency.currency_name == currency_name).first()
    if existing_currency:
        update_query = (
            update(Currency)
            .where(Currency.currency_name == currency_name)  # Фильтруем по имени валюты
            .values(rate=new_rate)  # Устанавливаем новое значение курса
        )
        session.execute(update_query)
        session.commit()
        return jsonify({'message': 'Валюта обновлена'}), 200
    else:
        return jsonify({'message': 'Валюта не найдена'}), 400


@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    currency_name = data['currency_name']


    currency = session.query(Currency).filter_by(currency_name=currency_name).first()
    if not currency:
        return jsonify({'message': 'Валюта не найдена'}), 404
    
    session.delete(currency)
    session.commit()
    session.close()
    return jsonify({'message': 'Валюта успешно удалена'}), 200


if __name__ == "__main__":
    port = 5001
    app.run(debug=True, port = port)


    


    
    
    