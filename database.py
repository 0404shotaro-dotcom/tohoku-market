import sqlite3
import hashlib
import os

DB_PATH = "tohoku_market.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ユーザーテーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 商品テーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'available',
            meetup_location TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (seller_id) REFERENCES users(id)
        )
    """)
    # 既存DBへのカラム追加（初回以降の起動用）
    try:
        c.execute("ALTER TABLE items ADD COLUMN image_path TEXT")
        conn.commit()
    except Exception:
        pass

    # チャットテーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items(id),
            FOREIGN KEY (sender_id) REFERENCES users(id)
        )
    """)

    # お気に入りテーブル
    c.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (item_id) REFERENCES items(id),
            UNIQUE(user_id, item_id)
        )
    """)

    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email: str, password: str, name: str) -> dict:
    """ユーザー登録。東北大学メールのみ許可。"""
    if not email.endswith("@tohoku.ac.jp"):
        return {"success": False, "error": "東北大学のメールアドレス (@tohoku.ac.jp) のみ登録できます。"}
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
            (email, hash_password(password), name)
        )
        conn.commit()
        return {"success": True}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "このメールアドレスはすでに登録されています。"}
    finally:
        conn.close()

def login_user(email: str, password: str) -> dict:
    """ログイン。"""
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password_hash = ?",
        (email, hash_password(password))
    ).fetchone()
    conn.close()
    if user:
        return {"success": True, "user": dict(user)}
    return {"success": False, "error": "メールアドレスまたはパスワードが違います。"}

def get_items(category=None, keyword=None, status="available"):
    conn = get_connection()
    query = """
        SELECT i.*, u.name as seller_name
        FROM items i JOIN users u ON i.seller_id = u.id
        WHERE i.status = ?
    """
    params = [status]
    if category and category != "すべて":
        query += " AND i.category = ?"
        params.append(category)
    if keyword:
        query += " AND (i.title LIKE ? OR i.description LIKE ?)"
        params += [f"%{keyword}%", f"%{keyword}%"]
    query += " ORDER BY i.created_at DESC"
    items = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(i) for i in items]

def post_item(seller_id, title, description, price, category, meetup_location, image_path=None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO items (seller_id, title, description, price, category, meetup_location, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (seller_id, title, description, price, category, meetup_location, image_path)
    )
    conn.commit()
    conn.close()

def get_item_by_id(item_id):
    conn = get_connection()
    item = conn.execute(
        "SELECT i.*, u.name as seller_name, u.email as seller_email FROM items i JOIN users u ON i.seller_id = u.id WHERE i.id = ?",
        (item_id,)
    ).fetchone()
    conn.close()
    return dict(item) if item else None

def send_message(item_id, sender_id, receiver_id, message):
    conn = get_connection()
    conn.execute(
        "INSERT INTO messages (item_id, sender_id, receiver_id, message) VALUES (?, ?, ?, ?)",
        (item_id, sender_id, receiver_id, message)
    )
    conn.commit()
    conn.close()

def get_messages(item_id, user_id):
    conn = get_connection()
    msgs = conn.execute("""
        SELECT m.*, u.name as sender_name FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.item_id = ? AND (m.sender_id = ? OR m.receiver_id = ?)
        ORDER BY m.created_at ASC
    """, (item_id, user_id, user_id)).fetchall()
    conn.close()
    return [dict(m) for m in msgs]

def toggle_favorite(user_id, item_id) -> bool:
    """お気に入り追加/解除。Trueなら追加済み。"""
    conn = get_connection()
    existing = conn.execute(
        "SELECT id FROM favorites WHERE user_id = ? AND item_id = ?",
        (user_id, item_id)
    ).fetchone()
    if existing:
        conn.execute("DELETE FROM favorites WHERE user_id = ? AND item_id = ?", (user_id, item_id))
        conn.commit()
        conn.close()
        return False
    else:
        conn.execute("INSERT INTO favorites (user_id, item_id) VALUES (?, ?)", (user_id, item_id))
        conn.commit()
        conn.close()
        return True

def get_favorites(user_id):
    conn = get_connection()
    items = conn.execute("""
        SELECT i.*, u.name as seller_name FROM favorites f
        JOIN items i ON f.item_id = i.id
        JOIN users u ON i.seller_id = u.id
        WHERE f.user_id = ?
        ORDER BY f.created_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(i) for i in items]

def get_my_items(user_id):
    conn = get_connection()
    items = conn.execute(
        "SELECT * FROM items WHERE seller_id = ? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(i) for i in items]
