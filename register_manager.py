from flask import Flask, jsonify, current_app, request
import sqlite3 as sql
from jsonschema import validate
import os
import bcrypt
import random
import time
import getpass
import uuid

app = Flask(__name__)
app.config["DATABASE"] = "./data/register.db"


def create_user(username, email, password):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    if not username or not email or not password:
        print("Error: Username, email, or password not provided.")
        return jsonify({"error": "Username, email, or password not provided."}), 400

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()
    cur.execute(
        "SELECT vX8hR_username, ajkSC_email FROM e50PMSBi_users WHERE vX8hR_username = ? OR ajkSC_email = ?",
        (username, email),
    )
    user = cur.fetchone()
    if user:
        print("Error: Username/email already in use.")
        return jsonify({"error": "Username/email already in use."}), 409

    salt = bcrypt.gensalt(rounds=14)
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    while True:
        user_id = str(uuid.uuid4())  # Generate UUID v7
        cur.execute(
            "SELECT Wj89c_uuid FROM e50PMSBi_users WHERE Wj89c_uuid = ?", (user_id,)
        )
        user = cur.fetchone()
        if not user:
            break
        else:
            continue
    cur.execute(
        "INSERT INTO e50PMSBi_users (Wj89c_uuid, vX8hR_username, ajkSC_email, D9K66_password) VALUES (?, ?, ?, ?)",
        (user_id, username, email, hashed_password.decode()),
    )
    con.commit()
    con.close()
    return jsonify({"message": "User created successfully"}), 201


def checkPW(username, password):
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return False

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()

    cur.execute(
        "SELECT D9K66_password FROM e50PMSBi_users WHERE vX8hR_username = ?",
        (username,),
    )
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode("utf-8"), user[0].encode("utf-8")):
        print("Password matched")
        con.close()
        return True
    else:
        time.sleep(round(random.uniform(0.2, 0.4), 3))  # Decoy delay
        print("Password did not match")
        con.close()
        return False


def changePW():
    if not os.path.exists(app.config["DATABASE"]):
        print("Error: Database does not exist.")
        return jsonify({"error": "Internal server error"}), 500

    con = sql.connect(app.config["DATABASE"])
    cur = con.cursor()

    # Decoy delay before checking the database
    time.sleep(round(random.uniform(0.2, 0.4), 3))

    cur.execute(
        "SELECT vX8hR_username, nzqCh_DoB FROM e50PMSBi_users WHERE vX8hR_username = ? AND nzqCh_DoB = ?",
        (username,),
    )
    user = cur.fetchone()

    while True:
        if user:
            time.sleep(round(random.uniform(0.2, 0.4), 3))
            print("Username matched.")
            newPass = request.form.get("new_password")
            confirmPass = request.form.get("confirm_password")

            if not newPass or not confirmPass:
                print("Error: New password or confirmation password not provided.")
                return (
                    jsonify(
                        {"error": "New password or confirmation password not provided."}
                    ),
                    400,
                )
            if newPass != confirmPass:
                time.sleep(
                    round(random.uniform(0.2, 0.4), 3)
                )  # Decoy delay before printing password mismatch
                print("Password did not match.")
                continue

            salt = bcrypt.gensalt(rounds=12)
            hashed_password = bcrypt.hashpw(newPass.encode("utf-8"), salt)
            cur.execute(
                "UPDATE e50PMSBi_users SET D9K66_password = ? WHERE vX8hR_username = ?",
                (hashed_password.decode(), username),
            )
            con.commit()
            print("Password updated successfully.")
            break
        else:
            time.sleep(
                round(random.uniform(0.2, 0.4), 3)
            )  # Decoy delay before printing username mismatch
            print("Username did not match.")
            break
    con.close()


if __name__ == "__main__":
    with app.app_context():

        def create_database():
            if not os.path.exists("./data"):
                os.makedirs("./data")

            con = sql.connect(app.config["DATABASE"])
            cur = con.cursor()

            cur.execute(
                """CREATE TABLE IF NOT EXISTS e50PMSBi_users (
                            Wj89c_uuid TEXT NOT NULL PRIMARY KEY,
                            vX8hR_username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            D9K66_password TEXT NOT NULL,
                            nzqCh_DoB TEXT NOT NULL
                        )"""
            )

            con.commit()
            con.close()

        create_database()
