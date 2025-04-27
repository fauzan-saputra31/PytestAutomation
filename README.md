## Setup

I use python 3.11,  if you have different python version please change it in Pipfile:

```
Pipfile

[requires]
python_version = "3.11"
```

Ensure you have
[pipenv already installed](https://automationhacks.io/2020/07/12/how-to-manage-your-python-virtualenvs-with-pipenv/):

```
# Activate virtualenv
pipenv shell
# Install all dependencies in your virtualenv
pipenv install
```

change API KEY and SECRET KEY in config.py:
```
API_KEY = 'API_KEY'
SECRET_KEY = 'SECRET_KEY'
```

to run the script use pytest command:
```
pytest spot_trading.py --html=report.html
```

or if you want specific cas use pytest -k command:
```
pytest spot_trading.py --html=report.html -k test_e2_market_order
```