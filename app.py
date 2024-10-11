from flask import Flask
import redis
import psycopg2

app = Flask(__name__)

# Redis connection
r = redis.Redis(host="redis", port=6379)

# PostgreSQL connection details
def get_db_version():
    try:
        conn = psycopg2.connect(
            host="your_postgresql_host",  # e.g., "localhost"
            database="your_database_name",  # e.g., "mydb"
            user="your_username",  # e.g., "postgres"
            password="your_password"  # e.g., "secret"
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return db_version
    except Exception as e:
        return f"Error connecting to PostgreSQL: {e}"


@app.route("/")
def home():
    # Increment Redis hit counter
    count = r.incr("hits")

    # Fetch PostgreSQL version
    db_version = get_db_version()

    # Check if db_version is fetched successfully
    if isinstance(db_version, tuple):
        return f"Connected to PostgreSQL! Database version: {db_version[0]}.<br>" \
               f"This page has been visited {count} times."
    else:
        return f"{db_version}.<br>This page has been visited {count} times."


if __name__ == "__main__":
    app.run(host="0.0.0.0")
