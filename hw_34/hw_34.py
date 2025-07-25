import sqlite3


DB_PATH = 'barbershop.db'
SQL_FILE_PATH = 'hw_34.sql'


def read_sql_file(filepath: str) -> str:
    """Функция для чтения sql скрипта."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def execute_script(conn: sqlite3.Connection, script: str) -> None:
    """Функция для выполнения sql скрипта."""
    cursor = conn.cursor()
    queries = [q.strip() for q in script.split(';') if q.strip()]
    for query in queries:
        cursor.execute(query)
    conn.commit()


def find_appointment_by_phone(conn: sqlite3.Connection, phone: str) -> list[tuple]:
    """Функция поиска записей на услугу по номеру телефона."""
    cursor = conn.cursor()
    query = '''
        SELECT appointments.id, 
        appointments.name, 
        appointments.phone, 
        appointments.date, 
        appointments.status, 
        appointments.comment,
        masters.first_name || ' ' || masters.last_name AS master_name,
        GROUP_CONCAT(s.title, ', ') AS services
        FROM appointments 
        JOIN masters ON masters.id = appointments.master_id
        JOIN appointments_services ON appointments.id = appointments_services.appointment_id
        JOIN services as s ON s.id = appointments_services.service_id
        WHERE appointments.phone = ?
        GROUP BY appointments.id
    '''

    cursor.execute(query, (phone,))
    return cursor.fetchall()


def find_appointment_by_comment(conn, comment_part: str) -> list[tuple]:
    """Функция поиска записей на услугу по части комментария."""
    cursor = conn.cursor()
    query = '''
        SELECT appointments.id, 
        appointments.name, 
        appointments.phone, 
        appointments.date, 
        appointments.status, 
        appointments.comment,
        masters.first_name || ' ' || masters.last_name AS master_name,
        GROUP_CONCAT(s.title, ', ') AS services
        FROM appointments 
        JOIN masters ON masters.id = appointments.master_id
        JOIN appointments_services ON appointments.id = appointments_services.appointment_id
        JOIN services as s ON s.id = appointments_services.service_id
        WHERE appointments.comment LIKE ?
        GROUP BY appointments.id
    '''
    cursor.execute(query, (f'%{comment_part}%',))
    return cursor.fetchall()


def create_appointment(
    conn,
    client_name: str,
    client_phone: str,
    master_name: str,
    services_list: list[str],
    comment: str = None,
) -> int:
    """Функция для создания новой записи."""
    # Получаем ID мастера
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM masters WHERE first_name || ' ' || last_name = ?", (master_name,))
    master_id = cursor.fetchone()[0]

    # Создаем запись
    cursor.execute(
        "INSERT INTO appointments (name, phone, master_id, status, comment) VALUES (?, ?, ?, 'ожидает', ?)",
        (client_name, client_phone, master_id, comment),
    )
    appointment_id = cursor.lastrowid

    # Связываем услуги
    placeholders = ', '.join('?' * len(services_list))
    cursor.execute(f'SELECT id FROM services WHERE title IN ({placeholders})', (*services_list,))

    services = cursor.fetchall()
    for service_id in services:
        cursor.execute(
            "INSERT INTO appointments_services (appointment_id, service_id) VALUES (?, ?)",
            (appointment_id, service_id[0]),
        )

    conn.commit()
    return appointment_id


def main():
    """Основная функция."""

    conn = sqlite3.connect(DB_PATH)
    script = read_sql_file(SQL_FILE_PATH)
    execute_script(conn, script)

    print('Поиск по телефону "999-999-0000":')
    appointments = find_appointment_by_phone(conn, '999-999-0000')
    for appointment in appointments:
        print(appointment)

    print('Поиск по части комментария "комментарий"')
    appointments = find_appointment_by_comment(conn, 'комментарий')
    for appointment in appointments:
        print(appointment)

    print("\nСоздание новой записи:")
    new_appointment_id = create_appointment(
        conn,
        'Андрей',
        '111-666-3333',
        'Барбер Шопович',
        ['Укладка', 'Окрашивание'],
        'Положительный',
    )
    print(f"Создана запись с ID: {new_appointment_id}")

    # Закрываем соединение
    conn.close()


if __name__ == "__main__":
    main()
