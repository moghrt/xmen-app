#!/bin/bash

# Build the project
#echo "Building the project..."
#python3.10 -m pip install -r requirements.txt

echo "Making migrations..."
python3.10 manage.py makemigrations --noinput || exit 1
python3.10 manage.py migrate --noinput || exit 1

echo "Collecting static..."
python3.10 manage.py collectstatic --noinput --clear || exit 1


echo "Starting server..."
python3.10 manage.py runserver 0.0.0.0:8000
