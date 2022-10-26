# currency

branch HomeWork_Lesson_05
 - Create Django Project Currency, flake8, GitHub Actions

branch HomeWork_Lesson_06
 - add models

branch HomeWork_Lesson_07
 - add templates, Base template

branch HomeWork_Lesson_08
 - add forms, CRUD-functions in views.py 

branch HomeWork_Lesson_09
 - class based views. reverse

branch HomeWork_Lesson_10
 - add model choices (Rate), 
 - add admin (Rate, Source, ContactUs), 
 - add custom date filter, 
 - add import/export, 
 - add silk plugin

branch HomeWork_Lesson_11
 - add model ResponseLog, 
 - add middleware to project (time statistics), 
 - set ContactUs and send email to console

branch HomeWork_Lesson_12
 - add export csv

branch HomeWork_Lesson_13
 - add login, logout
 - add change user profile
 - add change password, forgot password
 - add restriction on editing and deleting Rate, only for superuser

branch HomeWork_Lesson_14
 - create registration in new application accounts with confirmation by mail

branch HomeWork_Lesson_15
 - add a relationship between Rate and Source models

branch HomeWork_Lesson_16
 - prepare Celery and Rabbitmq.

branch HomeWork_Lesson_17
 - prepare Crontab based on Celerybeat.
 - create parser for PrivatBank API
 - create parser for MonoBank API
 - create parser for http://vkurse.dp.ua/
 - create parser for 3 other sites

branch HomeWork_Lesson_18
 - add Bootstrap.
 - add static and media
 - add crispy forms
 - add user avatar
 - add source logo

branch HomeWork_Lesson_19
 - add Pagination to rate_list
 - add Page_size to rate_list
 - add Django-Filter to rate_list
 - add ordering to rate_list
 - consolidate all this to GET query-string

branch HomeWork_Lesson_20
 - add djangorestframework
 - add to project new app 'api'
 - create rest view for Rate model 
   (generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView)
 - create rest view for Source model (ListAPIView)
 - create rest view for ContactUs model (ModelViewSet),
   with overrides method Create and send mail (celery task)

branch HomeWork_Lesson_21
 - add djangorestframework-simplejwt
 - add docs drf-yasg
 - add pagination
 - add filters and ordering (Rate, Source, ContactUs)
 - add version (v1) of Api application
 - add throttling
 - add Search filter to ContactUs

branch HomeWork_Lesson_22
 - add pytest and pytest-django
 - configuring pytest in project (pytest.ini, settings_test.py)
 - add json files (fixtures) for load in DB in tests
 - add conftest.py with fixtures (enable_db_access_for_all_tests, load_fixtures)
 - add command to Makefile: make pytest 
 - add tests (sanity.py, index.py, contactus.py, api.py: rate, contactus)

branch HomeWork_Lesson_23
 - add app/currency/management/commands/ (preparation for the archive parser task)
 - add pytest, pytest-cov, pytest-mock
 - apply coverage reporting to html
 - add to makefile commands coverage, show-coverage
 - add .github/workflows/pytest.yml
 - add fixtures api_client, api_client_auth (with refactoring api tests)
 - add tests for tasks with mocks: parse_privatbank, parse_monobank, parse_vkurse

branch HomeWork_ParseArchive
 - add app/currency/management/commands/parse_privatbank_archive.py
 - add function check_exist_and_create_rate to app/currency/utils.py

branch HomeWork_GunicornNginx
 - add gunicorn
 - add nginx
 - add uwsga
