mig:
	python manage.py makemigrations
	python manage.py migrate

super:
	python3 manage.py createsuperuser

app:
	pyhton3 manage.py startapp apps

