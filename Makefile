run:
	python manage.py migrate && python manage.py runserver 0.0.0.0:8088

freeze:
	pip freeze > requirements.txt

req:
	pip install -r requirements.txt

styling:
	flake8 . && black . && isort .

test:
	python manage.py test