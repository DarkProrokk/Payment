FROM python:3.11.6-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
CMD python manage.py migrate && \
    python manage.py initadmin && \
    python manage.py runserver 0.0.0.0:8000