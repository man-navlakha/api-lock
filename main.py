from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection (Replace with your Render DB URL)
DATABASE_URL = os.getenv("DATABASE_URL", "your_render_db_url_here")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route('/check', methods=['GET'])
def check_user():
    user_id = request.args.get('user_id')

    if not user_id or not user_id.isdigit():
        return jsonify({"error": "Invalid user_id"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT islocked FROM users WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    
    cur.close()
    conn.close()

    if result is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user_id": user_id, "islocked": result[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
