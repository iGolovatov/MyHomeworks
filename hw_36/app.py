# app.py
from flask import Flask, request, jsonify
from peewee import *
from datetime import datetime
from typing import Optional, Dict, Any
import json

from hw_36.models import Master, Appointment, initialize_db

# Инициализация базы данных
DB = SqliteDatabase('barbershop.db')


# Помощник для преобразования модели в словарь
def master_to_dict(master: Master) -> Dict[str, Any]:
    return {
        'id': master.id,
        'first_name': master.first_name,
        'last_name': master.last_name,
        'middle_name': master.middle_name,
        'phone': master.phone
    }


def appointment_to_dict(appointment: Appointment) -> Dict[str, Any]:
    return {
        'id': appointment.id,
        'client_name': appointment.client_name,
        'client_phone': appointment.client_phone,
        'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
        'master': master_to_dict(appointment.master),
        'status': appointment.status
    }


# Валидация данных
def validate_master_data(data: dict) -> tuple[bool, Optional[str]]:
    """Проверка данных мастера"""
    if not data.get('first_name'):
        return False, "first_name обязательное поле"
    if not data.get('last_name'):
        return False, "last_name обязательное поле"
    if not data.get('phone'):
        return False, "phone обязательное поле"
    if len(data['phone']) > 20:
        return False, "phone должен быть не более 20 символов"
    return True, None


def validate_appointment_data(data: dict) -> tuple[bool, Optional[str]]:
    """Проверка данных записи"""
    if not data.get('client_name'):
        return False, "client_name обязательное поле"
    if not data.get('client_phone'):
        return False, "client_phone обязательное поле"
    if not data.get('master_id'):
        return False, "master_id обязательное поле"
    if not data.get('date'):
        return False, "date обязательное поле"

    # Проверка формата даты
    try:
        datetime.fromisoformat(data['date'])
    except ValueError:
        return False, "date должен быть в формате ISO 8601"

    return True, None


# Создание приложения
app = Flask(__name__)


# Инициализация базы данных
@app.before_request
def before_request():
    DB.connect()


@app.after_request
def after_request(response):
    DB.close()
    return response


# Роуты для мастеров
@app.route('/masters', methods=['GET'])
def get_masters():
    """Получить список всех мастеров"""
    masters = Master.select()
    return (
        json.dumps({'masters': [master_to_dict(m) for m in masters]}, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'},
    )


@app.route('/masters/<int:id>', methods=['GET'])
def get_master(id: int):
    """Получить мастера по ID"""
    try:
        master = Master.get(Master.id == id)
        return (
            json.dumps({'master': master_to_dict(master)}, ensure_ascii=False),
            200,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


@app.route('/masters', methods=['POST'])
def create_master():
    """Создать нового мастера"""
    data = request.json
    is_valid, error = validate_master_data(data)

    if not is_valid:
        return (
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    try:
        master = Master.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            phone=data['phone']
        )
        return (
            json.dumps({'master': master_to_dict(master)}, ensure_ascii=False),
            201,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except IntegrityError:
        return (
            json.dumps({'error': 'Мастер с таким телефоном уже существует'}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


@app.route('/masters/<int:id>', methods=['PUT'])
def update_master(id: int):
    """Обновить данные мастера"""
    try:
        master = Master.get(Master.id == id)
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    data = request.json
    is_valid, error = validate_master_data(data)

    if not is_valid:
        return (
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    master.first_name = data.get('first_name', master.first_name)
    master.last_name = data.get('last_name', master.last_name)
    master.middle_name = data.get('middle_name', master.middle_name)
    master.phone = data.get('phone', master.phone)
    master.save()

    return (
        json.dumps({'master': master_to_dict(master)}, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'},
    )


@app.route('/masters/<int:id>', methods=['DELETE'])
def delete_master(id: int):
    """Удалить мастера"""
    try:
        master = Master.get(Master.id == id)
        master.delete_instance()
        return (
            json.dumps({'success': True}, ensure_ascii=False),
            204,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


# Роуты для записей
@app.route('/appointments', methods=['GET'])
def get_appointments():
    """Получить все записи с опциональной сортировкой"""
    sort_by = request.args.get('sort_by', 'date')
    direction = request.args.get('direction', 'asc')

    query = Appointment.select()

    if sort_by == 'date':
        if direction == 'desc':
            query = query.order_by(Appointment.date.desc())
        else:
            query = query.order_by(Appointment.date.asc())
    else:
        # По умолчанию сортируем по дате
        query = query.order_by(Appointment.date.asc())

    appointments = [appointment_to_dict(a) for a in query]
    return (
        json.dumps({'appointments': appointments}, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'},
    )


@app.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id: int):
    """Получить запись по ID"""
    try:
        appointment = Appointment.get(Appointment.id == id)
        return (
            json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
            200,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Appointment.DoesNotExist:
        return (
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


@app.route('/appointments/master/<int:master_id>', methods=['GET'])
def get_appointments_by_master(master_id: int):
    """Получить записи для заданного мастера"""
    try:
        master = Master.get(Master.id == master_id)
        appointments = [appointment_to_dict(a) for a in master.appointments]
        return (
            json.dumps({'appointments': appointments}, ensure_ascii=False),
            200,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


@app.route('/appointments', methods=['POST'])
def create_appointment():
    """Создать новую запись"""
    data = request.json
    is_valid, error = validate_appointment_data(data)

    if not is_valid:
        return (
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    try:
        master = Master.get(Master.id == data['master_id'])
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    try:
        appointment = Appointment.create(
            client_name=data['client_name'],
            client_phone=data['client_phone'],
            date=datetime.fromisoformat(data['date']),
            master=master,
            status=data.get('status', 'pending')
        )
        return (
            json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
            201,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Exception as e:
        return (
            json.dumps({'error': str(e)}, ensure_ascii=False),
            500,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


@app.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id: int):
    """Обновить запись"""
    try:
        appointment = Appointment.get(Appointment.id == id)
    except Appointment.DoesNotExist:
        return (
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    data = request.json
    is_valid, error = validate_appointment_data(data)

    if not is_valid:
        return (
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    try:
        master = Master.get(Master.id == data['master_id'])
    except Master.DoesNotExist:
        return (
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            400,
            {'Content-Type': 'application/json; charset=utf-8'},
        )

    appointment.client_name = data.get('client_name', appointment.client_name)
    appointment.client_phone = data.get('client_phone', appointment.client_phone)
    appointment.date = datetime.fromisoformat(data.get('date')) if data.get('date') else appointment.date
    appointment.master = master
    appointment.status = data.get('status', appointment.status)
    appointment.save()

    return (
        json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
        200,
        {'Content-Type': 'application/json; charset=utf-8'},
    )


@app.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id: int):
    """Удалить запись"""
    try:
        appointment = Appointment.get(Appointment.id == id)
        appointment.delete_instance()
        return (
            json.dumps({'success': True}, ensure_ascii=False),
            204,
            {'Content-Type': 'application/json; charset=utf-8'},
        )
    except Appointment.DoesNotExist:
        return (
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            {'Content-Type': 'application/json; charset=utf-8'},
        )


# Создание таблиц при запуске
@app.before_request
def create_tables():
    initialize_db()


if __name__ == '__main__':
    app.run(debug=True)
