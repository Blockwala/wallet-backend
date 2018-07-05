python manage.py makemigrations config
python manage.py migrate
uwsgi deploy_config.ini &
