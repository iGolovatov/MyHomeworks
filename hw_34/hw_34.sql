PRAGMA foreign_keys  = off;

BEGIN TRANSACTION;

-- Создание таблицы "Запись на услуги"
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    master_id INTEGER,
    status TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY (master_id) REFERENCES masters(id)
);

-- Создание таблицы "Мастера"
CREATE TABLE IF NOT EXISTS masters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    middle_name TEXT,
    phone TEXT NOT NULL
);

-- Создание таблицы "Услуги"
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    price REAL NOT NULL
);

-- Создание связующей таблицы "masters_services"
CREATE TABLE IF NOT EXISTS masters_services (
    master_id INTEGER,
    service_id INTEGER,
    PRIMARY KEY (master_id, service_id),
    FOREIGN KEY (master_id) REFERENCES masters(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);

-- Создание связующей таблицы "appointments_services"
CREATE TABLE IF NOT EXISTS appointments_services (
    appointment_id INTEGER,
    service_id INTEGER,
    PRIMARY KEY (appointment_id, service_id),
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);

-- Добавление данных о мастерах
INSERT INTO masters (first_name, last_name, middle_name, phone) VALUES
('Барбер', 'Шопович', 'Парикмахерский', '923-777-7788'),
('Сюзанна', 'Полубоксовна', 'Стрижкова', '913-700-0000');

-- Добавление данных об услугах
INSERT INTO services (title, description, price) VALUES
('Стрижка', 'Классическая стрижка', 1500),
('Бритье', 'Классическое бритье', 900),
('Укладка', 'Укладка волос', 700),
('Окрашивание', 'Окрашивание волос', 1500),
('Маникюр', 'Маникюр для мужчин', 800);

-- Связывание мастеров и услуг
INSERT INTO masters_services (master_id, service_id) VALUES
(1, 1), -- Барбер Парикмахерский оказывает услугу "Стрижка"
(1, 2), -- Барбер Парикмахерский оказывает услугу "Бритье"
(2, 3), -- Сюзанна Стрижкова оказывает услугу "Укладка"
(2, 4), -- Сюзанна Стрижкова оказывает услугу "Окрашивание"
(1, 5); -- Барбер Парикмахерский оказывает услугу "Маникюр"

-- Добавление записей на услуги
INSERT INTO appointments (name, phone, master_id, status, comment) VALUES
('Андрей', '996-379-2929', 1, 'подтверждена', 'Хороший комментарий'),
('Виктор', '999-999-0000', 2, 'подтверждена', 'Плохой комментарий'),
('Игорь', '923-333-1818', 1, 'ожидает', null),
('Григорий', '913-913-9113', 2, 'отменена', null);

-- Связывание записей и услуг
INSERT INTO appointments_services (appointment_id, service_id) VALUES
(1, 1), -- Андрей записался на "Стрижка"
(1, 2), -- Андрей записался на "Бритье"
(2, 3), -- Виктор записалась на "Укладку"
(3, 4), -- Игорь записалась на "Окрашивание"
(4, 5); -- Григорий записалась на "Маникюр"


-- Обычный индекс на поле `phone` в таблице `masters`
-- Ускоряет поиск мастера по телефону
CREATE INDEX idx_masters_phone ON masters (phone);

-- Обычный индекс на поле `title` в таблице `services`
-- Ускоряет выборку услуг по названию
CREATE INDEX idx_services_title ON services (title);

-- Составной индекс на поля (appointment_id, service_id) в таблице `appointments_services`
-- Ускоряет фильтрацию записей по записи на услугу и услуге
CREATE INDEX idx_appointments_services_appointment_service ON appointments_services (appointment_id, service_id);

-- Составной индекс на поля (status, date) в таблице `appointments`
-- Ускоряет получение записей по статусу и дате (например, "подтверждённые" сегодня)
CREATE INDEX idx_appointments_status_date ON appointments (status, date);

COMMIT;

PRAGMA foreign_keys = true;
