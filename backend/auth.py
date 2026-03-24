import bcrypt
from .db import get_db_connection

def register_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed.decode('utf-8'))
    )

    conn.commit()
    cur.close()
    conn.close()


def login_user(username, password):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        stored_password = user[1]

        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return user[0]

    return None