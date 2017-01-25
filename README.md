# sexist-scraper

### Setup postgres db
- Install postgres: [Postgress App](https://postgresapp.com/)
- Start postgres by launching Postgres in Applications folder
- Create scraper user and db
```
psql    #open psql prompt
create user scraper with password 'scraper'; 
create database scraper owner scraper;
\q      #quit psql
```

### Activate virtualenv and install deps
- In project root activate virtual environment   
```. /venv/bin/active```
- Install versioned dependencies from requirements.txt   
```pip install -r requirements.txt```