#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

find ./accounts/migrations -name "*.py" -not -name "__init__.py" -delete 2>/dev/null || true
find ./main_functionality/migrations -name "*.py" -not -name "__init__.py" -delete 2>/dev/null || true


python manage.py makemigrations accounts
python manage.py makemigrations main_functionality

python manage.py migrate

python manage.py collectstatic --no-input