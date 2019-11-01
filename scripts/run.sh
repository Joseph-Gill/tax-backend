#!/bin/bash
python -c "import time; time.sleep(3)" # Wait for postgres to start up
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver 0.0.0.0:8000
