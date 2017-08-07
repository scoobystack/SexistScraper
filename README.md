# sexist-scraper

### Setup postgres db
- Install postgres. Follow instructions here: [Postgress App](https://postgresapp.com/)
  - Be sure to add the PostgressApp bin dir to your PATH in your bash profile
```
export PATH="/Applications/Postgres.app/Contents/Versions/9.5/bin:$PATH"
```
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

### Create and activate virtualenv and install dependencies
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
