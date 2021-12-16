### Requirements:

- Python 3.7+ `(pip3 install -r requirements.txt)`
- Mysql 14+


### Setup development database

```
CREATE DATABASE quiz CHARACTER SET utf8 COLLATE utf8_bin;

CREATE USER 'quiz'@'localhost' IDENTIFIED BY 'quiz';

GRANT ALL PRIVILEGES ON * . * TO 'quiz'@'localhost';
```

### Setup django

`python3 manage.py migrate`

`python3 manage.py runserver`

`python3 manage.py createsuperuser`

### Test

`python3 manage.py test`