web: gunicorn codewithtm.wsgi --log-file -
worker: celery -A codewithtm worker
beat: celery -A codewithtm beat -S django