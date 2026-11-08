# Практикум Python ЛР15–18

Поточний етап — **ЛР16**, варіант **8**, **Музейний фонд**.
Це продовження ЛР15, не повний зразок майбутніх ЛР17–18.
Репозиторій: https://github.com/LitruzZz/course-monitoring-python-2026

## Реалізовано

- Device: name до 80 символів, serial до 40, унікальний.
- monitoring/migrations/0001_initial.py.
- Перелік /, пошук /?q=Фонд, деталь /devices/<int:pk>/.
- Лише GET/HEAD, відсутній об’єкт — 404, неправильний метод — 405.
- Admin: list_display name/serial, search_fields name/serial.
- Шаблони monitoring/ з автоматичним екрануванням і тегом url.
- 18 ізольованих тестів сторінок, пошуку, унікальності та прав.
- Flask-приклад для порівняння маршрутів і шаблонів.

Паспорти, мітки й вимірювання не додані. Їхній план — profile08.json.

## Середовище та запуск

Python 3.12.14, Django 6.1.2, SQLite 3.53.1. Залежності ЛР15 не змінені.
Використовуйте погоджений Python 3.12–3.14; активація .venv не обов’язкова.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Пароль навчального суперкористувача задайте інтерактивно. Реальні персональні
дані не потрібні. Через /admin/ додайте:

| name | serial |
|---|---|
| Фонд тканини | V08-A |
| Фонд дерево | V08-B |
| Вестибюль | V08-C |

Для швидкого відтворення замість ручного додавання:

```powershell
.venv\Scripts\python.exe manage.py loaddata profile08_devices
```

Під час підготовки ці три записи фактично створені через admin. Фікстура
додана для повторення без передачі БД. Звичайного навчального користувача
створіть у Users: is_staff=False, is_superuser=False. Паролі не зберігайте в Git.

## Перевірки

```powershell
.venv\Scripts\python.exe manage.py test monitoring -v 2
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.venv\Scripts\python.exe manage.py showmigrations monitoring
```

Фонд → V08-A, V08-B; ткан → V08-A; порожній q → усі три;
неіснуючий-зразок → порожній перелік. Пошук нічого не змінює.
Використано name__icontains. Поведінка регістру кирилиці залежить від SQLite;
підтримка всіх Unicode-перетворень регістру не заявляється.
POST із коректним CSRF-токеном → 405, Allow: GET, HEAD. Без токена
запит може раніше відхилити CSRF middleware як 403.

Звичайний користувач не входить до admin. Працівник без дозволів Device
не має доступу до її адмінсторінок (403) — це перевірено окремим тестом.
Синтетичні паролі тестів належать лише тимчасовій тестовій БД.

docs/protocol.txt, docs/verification.json — фактичні перевірки й схема.
docs/screenshots/ — справжні браузерні знімки. docs/settings_dictionary.* —
актуальний словник налаштувань.

## Flask

```powershell
.venv\Scripts\python.exe -m flask --app framework_examples.flask_app run --host 127.0.0.1 --port 5000
```

/ — HTML із render_template/url_for; /devices/1 — JSON;
/devices/wrong — 404. Django використовує path/include/render та тег url.

## Git і подання

Оновіть той самий GitHub-репозиторій, зберігши всі міграції. Після завантаження
додайте у звіт URL фактичного коміту /commit/... . Вебзавантаження створює
новий хеш: локальний хеш не слід видавати за віддалений.
У Git/ZIP не входять .venv, db.sqlite3, .env, кеші та робочі паролі.
SECRET_KEY береться зі змінної середовища або генерується для локального процесу.
Сервер запускається тільки на 127.0.0.1; це не публічне розгортання.
