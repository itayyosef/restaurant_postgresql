FROM python:3.10-slim

WORKDIR /project

RUN pip install Flask Flask-SQLAlchemy flask-login psycopg2-binary -U Flask-WTF email_validator

COPY . .

CMD python server.py