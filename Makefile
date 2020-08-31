.PHONY : clean env
ENV_NAME ?= test_env

clean:
	@py3clean .
env:
	virtualenv $(ENV_NAME ) -p python3
	pip install -r requirements.txt
superuser:
	python manage.py createsuperuser
migrations:
	python manage.py makemigrations
migrate: migrations
	python manage.py migrate