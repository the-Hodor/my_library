FROM python:3.10

# чтобы логи сразу выводились
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# копируем зависимости
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# копируем проект
COPY . .

CMD ["sh", "-c", "python manage.py migrate && gunicorn my_library.wsgi:application --bind 0.0.0.0:8000"]