SHELL := /bin/bash

manage_py := python app/manage.py

run:
	$(manage_py) runserver 0:8000

show_urls:
	$(manage_py) show_urls

makemigrations:
	$(manage_py) makemigrations

migrate:
	$(manage_py) migrate

migrate_and_run: makemigrations migrate run

shell_p:
	$(manage_py) shell_plus --print-sql

# SELERY
# запустить celery worker с выводом лога в консоль
celery_worker:
	cd app && celery -A settings worker --loglevel=INFO

# запустить celery beat с выводом лога в консоль
celery_beat:
	cd app && celery -A settings beat --loglevel=INFO

# запустить celery worker с очисткой очереди заданий без блокирования окна консоли (detach)
celery_worker_with_clean_detach:
	cd app && celery -A settings worker --purge -D

# запустить celery beat без блокирования окна консоли (detach)
celery_beat_with_detach:
	cd app && celery -A settings beat --detach

# Завершить все задачи и планирощик celery
celery_shutdown_all_active_tasks:
	cd app && celery -A tasks.updates.celery control shutdown

# Запустить тесты
pytest:
	pytest app/tests/

coverage:
	pytest --cov=app app/tests/ --cov-report html && coverage report --fail-under=60.0000

show-coverage:
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"
