release: python manage.py migrate
web: gunicorn csv_generation_service.wsgi
worker: celery -A csv_generation_service worker -l info