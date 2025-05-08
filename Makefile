mig:
	pyhton3 manage.py makemigrations
	pyhton3 manage.py migrate

super:
	python3 manage.py createsuperuser

app:
	pyhton3 manage.py startapp apps

