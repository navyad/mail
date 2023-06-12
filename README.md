# mail
Standalone Python script that integrates with Gmail API and performs some rule based operations on emails.

## Requirements
```python v3.11```

## Setup
1. create virtual environment and activate
    ```
    virtualenv -p python3.11 <env_name>
    cd <env_name>
    source bin/activate
    ```

2. clone the repo from https://github.com/navyad/mail (outside environment)
3. ```cd mail```
4. Install requirements using ```pip install -r requirements.txt```
5. ```export GMAIL_API_CREDS_FILE=<path-of-credentails.json>```

## Run script
```
❯ python app.py -h
usage: app.py [-h] [--create-tables] [--populate-db] [--apply-rule]

Apple mail app

options:
  -h, --help       show this help message and exit

Required arguments:
  --create-tables  Create table
  --populate-db    Populate the database
  --apply-rule     Apply rule

```

## Usage:
* Create tables
```python app.py --create-tables```
* Populate db with emails
```python app.py - --populate-db```
* Apply rule
```python app.py --apply-rule <rule description>```

  Note: Rule description can be found in rules.json 
  
  e.g.:
  ```python app.py --apply-rule  Rule_1```


## Run tests
```pytest```