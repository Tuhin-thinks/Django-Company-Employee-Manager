#!/bin/bash

# This script is used to launch a new instance of the application

# create a virtaulenv if not already exists and user has passed --create-env argument
if [ "$1" == "--create-env" ]; then
    if [ -d "venv" ]; then
        echo "Virtualenv already exists. Please remove it and try again. Or, use the existing virtualenv."
        exit 1
    fi
    echo "Creating virtualenv..."
    virtualenv venv
fi

# started with --launch-only argument
if [ "$1" == "--launch-only" ]; then
    launch
    exit 0
fi


launch() {
    # run the server
    python manage.py runserver
}

setup() {
# install the requirements
pip install -r requirements.txt

# create and run the migrations
python manage.py makemigrations
python manage.py migrate

# create superuser
DJANGO_SUPERUSER_EMAIL="admin@admin.com" \
DJANGO_SUPERUSER_PASSWORD=admin@1234 \
python manage.py createsuperuser --noinput
}

setup
launch
