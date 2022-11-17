SHELL := /bin/bash

docker_backend := docker exec -it backend

#manage_py := python app/manage.py
manage_py := docker exec -it backend python app/manage.py

run:
	$(manage_py) runserver 0:8000

show_urls:
	$(manage_py) show_urls

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

migrate_and_run: makemigrations migrate run

build:
	cp -n .env.example .env && docker-compose up -d --build

shell_p:
	$(manage_py) shell_plus --print-sql

# SELERY
# запустить celery worker с выводом лога в консоль
#celery_worker:
#	cd app && celery -A settings worker --loglevel=INFO

# запустить celery beat с выводом лога в консоль
#celery_beat:
#	cd app && celery -A settings beat --loglevel=INFO

# запустить celery worker с очисткой очереди заданий без блокирования окна консоли (detach)
#celery_worker_with_clean_detach:
#	cd app && celery -A settings worker --purge -D

# запустить celery beat без блокирования окна консоли (detach)
#celery_beat_with_detach:
#	cd app && celery -A settings beat --detach

# Завершить все задачи и планирощик celery
#celery_shutdown_all_active_tasks:
#	cd app && celery -A tasks.updates.celery control shutdown

# Запустить тесты
pytest:
	$(docker_backend) pytest app/tests/

coverage:
	$(docker_backend) pytest --cov=app app/tests/ --cov-report html && $(docker_backend) coverage report --fail-under=60.0000

show-coverage:
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"

# Запуск gunicorn
#gunicorn:
#	cd app && gunicorn settings.wsgi:application \
#						--bind 0.0.0.0:8002 \
#						--workers 8 \
#						--threads 2 \
#						--log-level debug \
#						--max-requests 1000 \
#						--timeout 10

# Запуск uwsgi
#uwsgi:
#	cd app && uwsgi --module=settings.wsgi:application \
#					--master \
#					--http=0.0.0.0:8002 \
#					--workers 8 \
#					--enable-threads \
#					--threads 2 \
#					--harakiri=10 \
#					--max-requests=1000 \
#					--log-format="[%(ftime)] uWSGI worker: %(wid) (pid: %(pid)) for request: %(method) %(uri) %(proto) response: %(status) (%(msecs) msec)"

# NGINX
#nginx_show_access_logs:
#	sudo tail /var/log/nginx/access.log -n 200

#nginx_show_error_logs:
#	sudo tail /var/log/nginx/error.log -n 200
