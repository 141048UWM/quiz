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

#Model bazy danych

![diagram_bazy](https://user-images.githubusercontent.com/93037037/146347022-6189f612-1888-456c-a267-5af9d3ff4284.png)
