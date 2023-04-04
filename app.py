from flask import Flask, jsonify
import sqlite3
from flask_cors import CORS, cross_origin
import os

DB_PATH = "/etc/x-ui/x-ui.db"
os.system(f"cp {DB_PATH} tmp/x-ui.db")

def get_db_connection():
    conn = sqlite3.connect('tmp/x-ui.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
CORS(app)

@app.route('/users/<id>', methods=['GET'])
def show_user(id):
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
        "error": False,
        "success": True,
        "user": user
    })

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
