pip install -r requirements-dev.txt && ^
autopep8 -r --in-place --aggressive --max-line-length=79 apps && ^
flake8 apps
