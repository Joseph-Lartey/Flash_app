from flask import Flask, render_template
import redis
import mysql.connector
import os

app = Flask(__name__)

# Redis setup (if needed)
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', '')
redis_client = redis.StrictRedis(
    host=redis_host, port=redis_port, password=redis_password, decode_responses=True
)

# MySQL configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'your_password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'visit_counter')

# Establish a connection to MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
    return connection

# Initialize the database by creating the 'visits' table if it doesn't exist
def init_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            visit_count INT NOT NULL
        );
    ''')
    cursor.execute('INSERT INTO visits (visit_count) VALUES (0) ON DUPLICATE KEY UPDATE visit_count=visit_count;')
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Increment the visit count
    cursor.execute('UPDATE visits SET visit_count = visit_count + 1;')
    connection.commit()

    # Retrieve the updated visit count
    cursor.execute('SELECT visit_count FROM visits;')
    visit_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # Optionally use Redis to cache visit count (this is just an example, remove if unnecessary)
    redis_client.set('visit_count', visit_count)

    return f"Hello! This page has been visited {visit_count} times."

if __name__ == '__main__':
    # Initialize the database before starting the app
    init_db()
    app.run(host='0.0.0.0', port=5000)
