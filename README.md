# sexist-scraper

### Setup postgres db
- Install postgres. Follow instructions here: [Postgress App](https://postgresapp.com/)
- Start postgres by launching Postgres in Applications folder
- Create scraper user and db
```
psql    #open psql prompt
create user scraper with password 'scraper'; 
create database scraper owner scraper;
\q      #quit psql 
```

### Install helpers
- Install [homebrew](https://brew.sh/)
- Install pip
```brew install pip```
- Install virtualenv
```pip install virtualenv```

### Create and activate virtualenv and install deps
- In project root create virtual environment
  - ```virtualenv venv```
- Activate virtual environment
  - ```. venv/bin/active```
- Install versioned dependencies from requirements.txt
  - ```pip install -r requirements.txt```
- Migrate db to latest schema
  - ```python manage.py migrate```
- Start the server
  - ```python manage.py runserver```