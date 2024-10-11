from flask import Flask
import os
import psycopg2
import redis


app = Flask(__name__)

r = redis.Redis(host="redis", port=6379)


# Get PostgreSQL connection details from environment variables
POSTGRES_URL = os.getenv('POSTGRES_URL')

@app.route('/')
def index():
    try:
        count = r.incr("hits")
        # Connect to PostgreSQL
        conn = psycopg2.connect(POSTGRES_URL)
        cursor = conn.cursor()

        # Execute a simple query
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        cursor.close()
        conn.close()

        return f"Connected to PostgreSQL! Database version: {db_version[0]}.<br>" \
            f"This page has been visited {count} times."

    except Exception as e:
        return f"Failed to connect to PostgreSQL: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

