from typing import Optional, Dict, Any

from flask import Blueprint, request, jsonify, Response
import json

from peewee import IntegrityError

from hw_37.models import Master
from hw_37.auth import is_valid_api_key, is_admin

masters_bp = Blueprint('masters', __name__)


# Помощник для преобразования модели в словарь
def master_to_dict(master: Master) -> Dict[str, Any]:
    return {
        'id': master.id,
        'first_name': master.first_name,
        'last_name': master.last_name,
        'middle_name': master.middle_name,
        'phone': master.phone
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


@masters_bp.route('/', methods=['GET'])
def get_masters():
    if not is_valid_api_key(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )

    masters = [m.to_dict() for m in Master.select()]
    return jsonify({"masters": masters})


@masters_bp.route('/<int:id>', methods=['GET'])
def get_master(id):
    if not is_valid_api_key(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Неверный API-ключ"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )

    try:
        master = Master.get(Master.id == id)
        return jsonify({"master": master.to_dict()})
    except Master.DoesNotExist:
        return jsonify({"error": "Мастер не найден"}), 404


@masters_bp.route('/', methods=['POST'])
def create_master():
    """Создать нового мастера"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )

    data = request.json
    is_valid, error = validate_master_data(data)

    if not is_valid:
        return Response(
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    try:
        master = Master.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            middle_name=data.get('middle_name'),
            phone=data['phone']
        )
        return Response(
            json.dumps({'master': master_to_dict(master)}, ensure_ascii=False),
            201,
            mimetype='application/json; charset=utf-8',
        )
    except IntegrityError:
        return Response(
            json.dumps({'error': 'Мастер с таким телефоном уже существует'}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )


@masters_bp.route('/<int:id>', methods=['PUT'])
def update_master(id: int):
    """Обновить данные мастера"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        master = Master.get(Master.id == id)
    except Master.DoesNotExist:
        return Response(
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )

    data = request.json
    is_valid, error = validate_master_data(data)

    if not is_valid:
        return Response(
            json.dumps({'error': error}, ensure_ascii=False),
            400,
            mimetype='application/json; charset=utf-8',
        )

    master.first_name = data.get('first_name', master.first_name)
    master.last_name = data.get('last_name', master.last_name)
    master.middle_name = data.get('middle_name', master.middle_name)
    master.phone = data.get('phone', master.phone)
    master.save()

    return Response(
        json.dumps({'master': master_to_dict(master)}, ensure_ascii=False),
        200,
        mimetype='application/json; charset=utf-8',
    )


@masters_bp.route('/<int:id>', methods=['DELETE'])
def delete_master(id: int):
    """Удалить мастера"""
    if not is_admin(request.headers.get('Api-Key')):
        return Response(
            json.dumps({"error": "Отказано в доступе. Требуются права администратора"}, ensure_ascii=False),
            status=403,
            mimetype="application/json; charset=utf-8"
        )
    try:
        master = Master.get(Master.id == id)
        master.delete_instance()
        return Response(
            json.dumps({'success': True}, ensure_ascii=False),
            204,
            mimetype='application/json; charset=utf-8',
        )
    except Master.DoesNotExist:
        return Response(
            json.dumps({'error': 'Мастер не найден'}, ensure_ascii=False),
            404,
            mimetype='application/json; charset=utf-8',
        )
