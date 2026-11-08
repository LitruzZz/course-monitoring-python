# Налаштування ЛР16

## BASE_DIR

`Path(__file__).resolve().parent.parent`

Кореневий каталог проєкту; база для шляхів до локальних файлів.

## SECRET_KEY

`DJANGO_SECRET_KEY або новий випадковий ключ процесу; значення не наводиться`

Ключ підпису. Значення береться з DJANGO_SECRET_KEY або генерується локально; реальний ключ у репозиторій і звіт не записується.

## DEBUG

`True`

Докладні діагностичні сторінки лише під час локального розроблення.

## ALLOWED_HOSTS

`['127.0.0.1', 'localhost']`

Дозволені імена хостів HTTP-запиту; лише loopback і localhost.

## INSTALLED_APPS

`['monitoring', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles']`

Застосунок monitoring підключений разом із шістьма стандартними застосунками Django.

## MIDDLEWARE

`['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']`

Послідовність проміжних обробників запиту й відповіді: безпека, сесії, загальні HTTP-правила, CSRF, користувач, повідомлення, захист від clickjacking.

## ROOT_URLCONF

`'config.urls'`

config.urls підключає monitoring.urls через include і зберігає admin/.

## TEMPLATES

`[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]`

DjangoTemplates; окремих каталогів немає, шаблони застосунків дозволені. Контекстні процесори передають запит, користувача/дозволи й повідомлення.

## WSGI_APPLICATION

`'config.wsgi.application'`

Точка входу для WSGI-сумісного сервера; ASGI окремо оголошено в config/asgi.py.

## DATABASES

`{'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}`

SQLite-файл db.sqlite3 в BASE_DIR. База створюється міграціями та не входить до Git/ZIP.

## AUTH_PASSWORD_VALIDATORS

`[{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'}, {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'}, {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]`

Стандартні перевірки пароля: схожість із даними користувача, мінімальна довжина, поширений пароль і пароль лише з цифр. Паролів у коді немає.

## LANGUAGE_CODE

`'uk'`

Українська локалізація інтерфейсів Django.

## TIME_ZONE

`'Europe/Kyiv'`

Часовий пояс проєкту — Київ.

## USE_I18N

`True`

Увімкнена система перекладів і локалізації.

## USE_TZ

`True`

Увімкнена робота з часовими поясами; майбутні вимірювання матимуть часову зону.

## STATIC_URL

`'static/'`

URL-префікс статичних ресурсів CSS/JS/зображень.

## MAILERS

`{'default': {'BACKEND': 'django.core.mail.backends.console.EmailBackend'}}`

Стандартний поштовий механізм цього згенерованого проєкту виводить листи в консоль; зовнішній поштовий сервіс не налаштовано.
