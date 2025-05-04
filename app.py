import sqlite3
from flask import Flask, jsonify, request, session
from jwt_util import generate_token, decode_token
from db import init_db, insert_token, token_exists, verify_user, update_admin_credentials
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = 'session'  # 用于session加密
init_db()

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if verify_user(username, password):
        session['logged_in'] = True
        return jsonify({"success": True})
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('logged_in', None)
    return jsonify({"success": True})

@app.route("/check-auth")
def check_auth():
    return jsonify({"logged_in": session.get('logged_in', False)})

@app.route("/generate", methods=["POST"])
def generate():
    if not session.get('logged_in'):
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.get_json()
    days = data.get("days", 1)  # 默认1天
    token = generate_token(days)
    insert_token(token)
    return jsonify({"token": token})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Token is required"}), 400

    if not token_exists(token):
        return jsonify({"valid": False, "reason": "Token not found"}), 404

    decoded = decode_token(token)
    if not decoded:
        return jsonify({"valid": False, "reason": "Invalid token"}), 400

    return jsonify({"valid": True, "created_at": decoded["created_at"]})

@app.route("/list")
def get_tokens():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    offset = (page - 1) * size

    conn = sqlite3.connect("database.db")  # 修改这里，使用database.db
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM card_keys")  # 修改表名为card_keys
    total = cursor.fetchone()[0]

    cursor.execute("SELECT id, token, created_at FROM card_keys ORDER BY id DESC LIMIT ? OFFSET ?", (size, offset))  # 修改表名为card_keys
    rows = cursor.fetchall()
    conn.close()

    tokens = [{"id": r[0], "token": r[1], "created_at": r[2]} for r in rows]
    return jsonify({
        "data": tokens,
        "total": total,
        "page": page,
        "size": size
    })

@app.route("/update-admin", methods=["POST"])
def update_admin():
    if not session.get('logged_in'):
        return jsonify({"error": "未登录"}), 401
        
    data = request.get_json()
    new_username = data.get("username")
    new_password = data.get("password")
    
    if not new_username or not new_password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
        
    if update_admin_credentials(new_username, new_password):
        # 更新成功后更新session
        session['logged_in'] = False
        return jsonify({"success": True})
    else:
        return jsonify({"error": "更新失败"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9840)
