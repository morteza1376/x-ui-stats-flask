from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS, cross_origin
import os
import time

def get_db_connection():
    conn = sqlite3.connect('tmp/x-ui.db')
    conn.row_factory = sqlite3.Row
    return conn

def update_db():
    DB_PATH = "/etc/x-ui/x-ui.db"
    os.system(f"cp {DB_PATH} tmp/x-ui.db")

    with open('db_update_time', 'w') as f:
        f.write(str(int(time.time())))

def get_last_db_update_time():
    with open('db_update_time', 'r') as f:
        return f.read()


app = Flask(__name__)
CORS(app)

@app.route('/users/<id>', methods=['GET'])
def show_user(id):
    # Check for database update Time
    last_db_update_time = get_last_db_update_time()
    if int(time.time() - int(last_db_update_time)) > 60:
        update_db()

    conn = get_db_connection()
    query = f'SELECT * FROM "client_traffics" WHERE LOWER(email)=?'
    user = conn.execute(query, [id.lower()]).fetchall()
    conn.close()

    if not user:
        return jsonify({
            "error": True,
            "message": "User not found"
        })
    user = dict(user[0])
    return jsonify({
        "db_updated_at": last_db_update_time,
        "error": False,
        "success": True,
        "user": user
    })

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
