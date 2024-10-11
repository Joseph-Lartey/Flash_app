from flask import Flask
import redis
import mysql.connector

app = Flask(__name__)

# Redis setup
r = redis.Redis(host="redis", port=6379)

# MySQL setup
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="rootpassword",
    database="visitor_db"
)
cursor = db.cursor()

@app.route("/")
def home():
    # Update Redis count
    redis_count = r.incr("hits")

    # Fetch the current MySQL count
    cursor.execute("SELECT count FROM visit_count WHERE id = 1")
    result = cursor.fetchone()

    if result:
        mysql_count = result[0] + 1
        cursor.execute("UPDATE visit_count SET count = %s WHERE id = 1", (mysql_count,))
        db.commit()
    else:
        mysql_count = 1
        cursor.execute("INSERT INTO visit_count (count) VALUES (1)")
        db.commit()

    return f"This page has been visited {redis_count} times (Redis) and {mysql_count} times (MySQL)."

if __name__ == "__main__":
    app.run(host="0.0.0.0")
