import bcrypt
import json
import os

USER_FILE = "users.json"


# ---------------- LOAD USERS ----------------
def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


# ---------------- SAVE USERS ----------------
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


# ---------------- REGISTER USER ----------------
def register_user(email, password):
    users = load_users()

    if email in users:
        return False

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[email] = hashed_pw.decode()   # store as string

    save_users(users)
    return True


# ---------------- AUTHENTICATE USER ----------------
def authenticate(email, password):
    users = load_users()

    if email not in users:
        return False

    return bcrypt.checkpw(
        password.encode(),
        users[email].encode()
    )
