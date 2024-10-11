# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Install psycopg2 for PostgreSQL connection
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install psycopg2

CMD ["python", "app.py"]


