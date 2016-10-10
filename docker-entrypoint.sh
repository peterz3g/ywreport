#/code/manage.py syncdb --noinput
#/usr/local/bin/gunicorn config.wsgi:application -w 2 -b :8000

today=`date +"%Y%m%d"`
python /code/manage.py makemigrations
python /code/manage.py migrate
python /code/manage.py runserver 0.0.0.0:8000 | tee /code/${today}.log



