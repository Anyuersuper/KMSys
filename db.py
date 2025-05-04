import sqlite3
from datetime import datetime
import hashlib

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS card_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at DATETIME NOT NULL
        )
    ''')
    
    # 创建默认管理员账户
    username = "yuer"
    password = "yuerpass"
    c.execute("SELECT id FROM users WHERE username = " + "?", (username,))
    # 检查是否存在管理员账户，如果不存在则创建
    if not c.fetchone():
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        c.execute("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                 (username, hash_password, datetime.utcnow()))
    
    conn.commit()
    conn.close()

def insert_token(token):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO card_keys (token, created_at) VALUES (?, ?)", (token, datetime.utcnow()))
    conn.commit()
    conn.close()

def token_exists(token):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id FROM card_keys WHERE token = ?", (token,))
    result = c.fetchone()
    conn.close()
    return result is not None

def list_tokens():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT id, token, created_at FROM card_keys")
    tokens = c.fetchall()
    conn.close()
    return tokens

def verify_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password))
    result = c.fetchone()
    conn.close()
    return result is not None

def update_admin_credentials(new_username, new_password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    hash_password = hashlib.sha256(new_password.encode()).hexdigest()
    
    try:
        # 更新管理员用户信息
        c.execute("UPDATE users SET username = ?, password = ? WHERE username = 'admin' OR username = ?", 
                 (new_username, hash_password, new_username))
        conn.commit()
        success = c.rowcount > 0
    except sqlite3.Error:
        success = False
    finally:
        conn.close()
    
    return success
