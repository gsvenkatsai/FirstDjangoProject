release : python manage.py migrate
web: gunicorn project1.wsgi
worker: celery -A project1 worker
