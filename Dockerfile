# указывам образ от которого мы будем наследоваться
FROM python:3.8

# указываем рабочую директорию проекта в контейнере
WORKDIR /app/build

# добавляем в PYTHONPATH репозиторий app (избавляемся от cd app && )
ENV PYTHONPATH /app/build/app

# устанавливаем необходимые библиотеки через apt
# RUN apt-get update -y && apt-get install -y --no-install-recommends \
#    default-libmysqlclient-dev && \
#    rm -rf /var/lib/apt/lists/*

# устанавливаем библиотеку iputils-ping (для ping)
RUN apt update -y && apt install -y iputils-ping

# копируем в контейнер файл requirements.txt и устанавливаем по нему все библиотеки и зависимости
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# копируем в контейнер всю папку с проектом
COPY . .

# запускаем процессы в контейнере

# команда запуска "процесса-заглушки"
# CMD ["tail", "-f", "/dev/null"]

# команда запуска runserver
#CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]

# команда запуска gunicorn
CMD ["gunicorn", \
     "settings.wsgi:application", \
     "--bind=0.0.0.0:8000", \
     "--workers", "8", \
     "--threads", "2", \
     "--log-level", "debug", \
     "--max-requests", "1000", \
     "--timeout", "10"]

#ENTRYPOINT
