# e-store-backend

#### How to run?
1. create virtual environment and activate it
2. install requierements `pip install -r requirements.txt`
3. create `.env` file beside `settings.py` file and set db environment variables (there is an example file .env.example which should be used in .env)
4. run migrate command `python manage.py migrate`
5. create superuser `python manage.py createsuperuser`
6. run project `python manage.py runserver`
7. project will open up at [http://localhost:8000](http://localhost:8000) 

#### Go to [http://localhost:8000/swagger](http://localhost:8000/swagger) to see REST APIs
