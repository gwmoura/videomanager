# videomanager

#### Dependencies

* Django 1.11
* Python 3

#### Install

* `pip install -r requirements.txt`
* `python manage.py migrate`

#### Using Docker
* `docker-compose build`
* `docker-compose run --rm web python manage.py migrate`
* `docker-compose up`
* open your browser on `http://localhost:5000/admin`
