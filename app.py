from flask import Flask, render_template, request
import redis
import mysql.connector
import os

app = Flask(__name__)

# Redis setup
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_password = os.getenv('REDIS_PASSWORD', '')

redis_client = redis.StrictRedis(
    host=redis_host, 
    port=redis_port, 
    password=redis_password, 
    decode_responses=True
)



# MySQL setup
db_config = {
    'user': os.getenv('MYSQL_USER', 'your_mysql_user'),
    'password': os.getenv('MYSQL_PASSWORD', 'your_mysql_password'),
    'host': os.getenv('MYSQL_HOST', 'your_mysql_host'),
    'database': os.getenv('MYSQL_DB', 'your_database')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Route to track user visits
@app.route('/')
def index():
    user_ip = request.remote_addr  # Use user's IP address as a temporary identifier
    
    # Check if user has visited before using Redis
    if not redis_client.exists(user_ip):
        redis_client.set(user_ip, 0)

    # Increment visit count for this user
    redis_client.incr(user_ip)
    visit_count = redis_client.get(user_ip)

    # Insert or update visit count in MySQL database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user already exists in MySQL and update visit count
    cursor.execute("SELECT * FROM visits WHERE user_id = %s", (user_ip,))
    result = cursor.fetchone()

    if result:
        cursor.execute("UPDATE visits SET visit_count = %s WHERE user_id = %s", (visit_count, user_ip))
    else:
        cursor.execute("INSERT INTO visits (user_id, visit_count) VALUES (%s, %s)", (user_ip, visit_count))

    conn.commit()
    cursor.close()
    conn.close()

    # Render template with visit count for this user
    return render_template('index.html', user_id=user_ip, visit_count=visit_count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
