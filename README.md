# Events demo app

## Requirements

- [Pipenv](https://pipenv.pypa.io/en/latest/) for dependency management

## Installation and Run

- Clone repo

	`git clone git@github.com:avallbona/demo-events-app.git`
	
- Setup virtual environment

```bash
cd demo-events-app
pipenv install    
```

- Activate virtualenv

```bash
pipenv shell
```
    
- Apply migrations

```bash
python manage.py migrate 
```
    
- Run server

```bash
python manage.py runserver  
```


## Open app in the browser

```bash
firefox http://127.0.0.1:8000/
```


## Additional info

- Create a super user in order to access the django administrator

```bash
python manage.py createsuperuser
```

- Events dated before the current day will not be displayed as they are considered expired. The event list only shows future events.