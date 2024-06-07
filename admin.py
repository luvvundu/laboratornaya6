from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Postgres import sqlal
from Postgres.sqlal import session, Currency, Admin
import asyncio
from aiohttp import web
from sqlalchemy import update

app = Flask(__name__)


@app.route('/check', methods=['GET'])
def convert_currency():
    userID = request.args.get('user')
    # Проверяем, является ли пользователь администратором
    admin = session.query(Admin).filter(Admin.chat_id == str(userID)).first()
    if not admin:
        return jsonify({'error': 'Вам не разрешен доступ к инструментам администратора'}), 403
    else:
        session.close()
        return jsonify({'message': 'Приступаю к работе с администратором'}), 200

if __name__ == "__main__":
    port = 5000
    app.run(debug=True, port=port)
