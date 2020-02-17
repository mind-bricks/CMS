pip install -r requirements-dev.txt && ^
python manage.py makemigrations && ^
autopep8 -r --in-place --aggressive --max-line-length=79 apps && ^
flake8 apps && ^
python manage.py compilemessages && ^
python manage.py test
