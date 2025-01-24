from flask import Flask, redirect, render_template, request, jsonify
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import register_manager as rm

app_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="main_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = b"6HlQfWhu03PttohW;apl"

global csp
csp = {
    "default-src": "'self'",
    "style-src": "'self' https://cdn.jsdelivr.net/",
    "script-src": "'self' https://cdn.jsdelivr.net/",
    "img-src": "'self' data: *",
    "media-src": "'self'",
    "font-src": "'self' data:",
    "connect-src": "'self'",
    "object-src": "'self'",
    "worker-src": "'self'",
    "frame-src": "'none'",
    "form-action": "'self'",
    "manifest-src": "'self'",
}


@app.route("/index.html", methods=["GET"])
def root():
    return redirect("/", 302)


@app.route("/", methods=["GET"])
@csp_header(
    csp=csp,
)
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        rm.create_user(username, email, password)
        return redirect("/register_success", 302)

    return render_template("register.html")


@app.route("/register_success", methods=["GET"])
def register_success():
    return "User created successfully"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
