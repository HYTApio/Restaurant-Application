import secrets
from flask import session, request, abort
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql_code = "SELECT id, password, role FROM users WHERE name=:username"
    result = db.session.execute(sql_code, {"username":username})
    user = result.fetchone()
    if not user:
        return False

    if check_password_hash(user[1], password):
        session["user_id"] = user[0]
        session["user_name"] = username
        session["user_role"] = user[2]
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False


def logout():
    del session["user_id"]
    del session["user_name"]
    del session["user_role"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql_code = "INSERT INTO users (name, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql_code, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)
    
def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)