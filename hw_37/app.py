from peewee import *
from flask import Flask, request
from blueprints.masters.routes import masters_bp
from blueprints.appointments.routes import appointments_bp
from models import initialize_db

# Инициализация базы данных
DB = SqliteDatabase('barbershop.db')

app = Flask(__name__)

app.register_blueprint(masters_bp, url_prefix='/masters')
app.register_blueprint(appointments_bp, url_prefix='/appointments')

initialize_db()


# Инициализация базы данных
@app.before_request
def before_request():
    print(request.headers)
    DB.connect()


@app.after_request
def after_request(response):
    DB.close()
    return response


if __name__ == '__main__':
    app.run(debug=True)
