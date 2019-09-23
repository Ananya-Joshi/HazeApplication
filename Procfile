web: gunicorn app:app --log-level=debug
release: python manage.py db upgrade
clock: python jobs.py