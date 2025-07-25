from peewee import *
from datetime import datetime

# Инициализация базы данных
DB = SqliteDatabase('barbershop.db')


# Определение моделей
class Master(Model):
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    middle_name = CharField(max_length=50, null=True)
    phone = CharField(max_length=20, unique=True)

    class Meta:
        database = DB


class Service(Model):
    title = CharField(max_length=100, unique=True)
    description = TextField(null=True)
    price = DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        database = DB


class Appointment(Model):
    client_name = CharField(max_length=100, null=False)
    client_phone = CharField(max_length=20, null=False)
    date = DateTimeField(default=datetime.now)
    master = ForeignKeyField(Master, backref='appointments')
    status = CharField(max_length=20, default='pending')

    class Meta:
        database = DB


class MasterService(Model):
    master = ForeignKeyField(Master)
    service = ForeignKeyField(Service)

    class Meta:
        database = DB
        primary_key = CompositeKey('master', 'service')


class AppointmentService(Model):
    appointment = ForeignKeyField(Appointment)
    service = ForeignKeyField(Service)

    class Meta:
        database = DB
        primary_key = CompositeKey('appointment', 'service')


# Создание таблиц и заполнение данными
def initialize_db():
    try:
        DB.connect()
        DB.create_tables([Master, Service, Appointment, MasterService, AppointmentService], safe=True)

        # Мастера
        for data in [
            {'first_name': 'Иван', 'last_name': 'Иванов', 'phone': '+79991234567'},
            {'first_name': 'Петр', 'last_name': 'Петров', 'phone': '+79997654321'},
            {'first_name': 'Анна', 'last_name': 'Смирнова', 'phone': '+79991122334'},
        ]:
            Master.get_or_create(**data)

        # Услуги
        for data in [
            {'title': 'Стрижка', 'price': 1500.00},
            {'title': 'Уход за бородой', 'price': 1000.00},
            {'title': 'Маникюр', 'price': 800.00},
            {'title': 'Покраска', 'price': 2000.00},
        ]:
            Service.get_or_create(**data)

        # Связи мастер-услуга
        masters = Master.select()
        services = Service.select()
        for master in masters:
            for service in services:
                MasterService.get_or_create(master=master, service=service)

        # Заявки
        appointments_data = [
            {
                'client_name': 'Алексей',
                'client_phone': '+79999999999',
                'date': datetime(2025, 5, 25, 14, 0),
                'master_id': 1,
                'services': [1, 2]
            },
            {
                'client_name': 'Мария',
                'client_phone': '+79998888888',
                'date': datetime(2025, 5, 26, 10, 0),
                'master_id': 2,
                'services': [3, 4]
            },
            {
                'client_name': 'Дмитрий',
                'client_phone': '+79997777777',
                'date': datetime(2025, 5, 27, 15, 0),
                'master_id': 3,
                'services': [1, 4]
            }
        ]

        for data in appointments_data:
            master = Master.get(Master.id == data['master_id'])
            appointment = Appointment.get_or_create(
                client_name=data['client_name'],
                client_phone=data['client_phone'],
                date=data['date'],
                master=master,
                defaults={'status': 'pending'},
            )[0]

            for service_id in data['services']:
                service = Service.get(Service.id == service_id)
                AppointmentService.get_or_create(appointment=appointment, service=service)

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        DB.close()
