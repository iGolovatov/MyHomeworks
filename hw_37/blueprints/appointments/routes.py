from datetime import datetime
from typing import Dict, Any, Optional

from flask import Blueprint, request, jsonify, Response
import json

from hw_37.blueprints.masters.routes import master_to_dict
from hw_37.models import Appointment, Master
from hw_37.auth import is_valid_api_key, is_admin

appointments_bp = Blueprint('appointments', __name__)


def appointment_to_dict(appointment: Appointment) -> Dict[str, Any]:
    return {
        'id': appointment.id,
        'client_name': appointment.client_name,
        'client_phone': appointment.client_phone,
        'date': appointment.date.strftime('%Y-%m-%d %H:%M:%S'),
        'master': master_to_dict(appointment.master),
        'status': appointment.status
    }


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


@appointments_bp.route('/', methods=['GET'])
def get_appointments():
    if not is_valid_api_key(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )

    sort_by = request.args.get('sort_by', 'date')
    direction = request.args.get('direction', 'asc')

    query = Appointment.select()
    if sort_by == 'date':
        query = query.order_by(Appointment.date.desc() if direction == 'desc' else Appointment.date.asc())

    appointments = [a.to_dict() for a in query]
    return jsonify({"appointments": appointments})


@appointments_bp.route('/<int:id>', methods=['GET'])
def get_appointment(id: int):
    """Получить запись по ID"""
    if not is_valid_api_key(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        appointment = Appointment.get(Appointment.id == id)
        return Response(
            json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
            200,
            mimetype='application/json; charset=utf-8',
        )
    except Appointment.DoesNotExist:
        return Response(
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )


@appointments_bp.route('/master/<int:master_id>', methods=['GET'])
def get_appointments_by_master(master_id: int):
    """Получить записи для заданного мастера"""
    if not is_valid_api_key(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        master = Master.get(Master.id == master_id)
        appointments = [appointment_to_dict(a) for a in master.appointments]
        return Response(
            json.dumps({'appointments': appointments}, ensure_ascii=False),
            200,
            mimetype='application/json; charset=utf-8',
        )
    except Master.DoesNotExist:
        return Response(
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )


@appointments_bp.route('/', methods=['POST'])
def create_appointment():
    """Создать новую запись"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    data = request.json
    is_valid, error = validate_appointment_data(data)

    if not is_valid:
        return Response(
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    try:
        master = Master.get(Master.id == data['master_id'])
    except Master.DoesNotExist:
        return Response(
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    try:
        appointment = Appointment.create(
            client_name=data['client_name'],
            client_phone=data['client_phone'],
            date=datetime.fromisoformat(data['date']),
            master=master,
            status=data.get('status', 'pending')
        )
        return Response(
            json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
            201,
            mimetype='application/json; charset=utf-8',
        )
    except Exception as e:
        return Response(
            json.dumps({'error': str(e)}, ensure_ascii=False),
            500,
            mimetype='application/json; charset=utf-8',
        )


@appointments_bp.route('/<int:id>', methods=['PUT'])
def update_appointment(id: int):
    """Обновить запись"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        appointment = Appointment.get(Appointment.id == id)
    except Appointment.DoesNotExist:
        return Response(
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )

    data = request.json
    is_valid, error = validate_appointment_data(data)

    if not is_valid:
        return Response(
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    try:
        master = Master.get(Master.id == data['master_id'])
    except Master.DoesNotExist:
        return Response(
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    appointment.client_name = data.get('client_name', appointment.client_name)
    appointment.client_phone = data.get('client_phone', appointment.client_phone)
    appointment.date = datetime.fromisoformat(data.get('date')) if data.get('date') else appointment.date
    appointment.master = master
    appointment.status = data.get('status', appointment.status)
    appointment.save()

    return Response(
        json.dumps({'appointment': appointment_to_dict(appointment)}, ensure_ascii=False),
        200,
        mimetype='application/json; charset=utf-8',
    )


@appointments_bp.route('/<int:id>', methods=['DELETE'])
def delete_appointment(id: int):
    """Удалить запись"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        appointment = Appointment.get(Appointment.id == id)
        appointment.delete_instance()
        return Response(
            json.dumps({'success': True}, ensure_ascii=False),
            204,
            mimetype='application/json; charset=utf-8',
        )
    except Appointment.DoesNotExist:
        return Response(
            json.dumps({'error': 'Запись не найдена'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )
