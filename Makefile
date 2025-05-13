mig:
	python manage.py makemigrations
	python manage.py migrate

super:
	python3 manage.py createsuperuser

app:
	pyhton3 manage.py startapp apps

data:
	pyhton3 manage.py loaddata users.json
	pyhton3 manage.py loaddata posts.json
	pyhton3 manage.py loaddata comments.json

stub:
	pip3 install django-stubs