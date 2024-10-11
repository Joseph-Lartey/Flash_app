from flask import Flask
import redis
import mysql.connector
import os

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# MySQL setup
db = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'user'),  # Set to 'user' as per docker-compose
    password=os.getenv('MYSQL_PASSWORD', 'your_password'),  # Set to 'your_password'
    database=os.getenv('MYSQL_DATABASE', 'visit_counter')
)


# Check if table exists in MySQL, and create if not
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visit_count (
        id INT AUTO_INCREMENT PRIMARY KEY,
        count INT NOT NULL
    );
''')
cursor.execute('SELECT * FROM visit_count')
result = cursor.fetchone()
if not result:
    cursor.execute('INSERT INTO visit_count (count) VALUES (0)')
    db.commit()


@app.route('/')
def home():
    # Increment hits in Redis
    try:
        count = r.incr('hits')
    except redis.exceptions.ConnectionError:
        # If Redis is down, use MySQL
        cursor.execute('SELECT count FROM visit_count WHERE id = 1')
        count = cursor.fetchone()[0] + 1

        # Update MySQL with new count
        cursor.execute('UPDATE visit_count SET count = %s WHERE id = 1', (count,))
        db.commit()

    return f"This page has been visited {count} times."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
