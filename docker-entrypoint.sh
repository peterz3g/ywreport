#/code/manage.py syncdb --noinput
#/usr/local/bin/gunicorn config.wsgi:application -w 2 -b :8000
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000


