from flask import Flask, redirect, render_template, request, jsonify, session
from flask_session import Session
import requests
from flask_wtf import CSRFProtect
from flask_csp.csp import csp_header
import logging
import register_manager as rm
import os
from forms import RegistrationForm, LoginForm
from flask_wtf.csrf import generate_csrf

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

# Flask-Session configuration
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24).hex()
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = 3600  # 1 hour
Session(app)

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
    app_log.debug(f"Session state at /: {session}")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
@csp_header(
    csp=csp,
)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        response, status_code = rm.create_user(username, email, password)
        if status_code == 200:
            session.clear()  # Clear the old session
            session["username"] = username  # Set the new session data
            csrf_token = generate_csrf()  # Generate the CSRF token
            app_log.debug(f"CSRF token after registration: {csrf_token}")
            app_log.debug(f"Session state after registration: {session}")
            return redirect("/register_success", 302)

    return render_template("register.html", form=form)


@app.route("/register_success", methods=["GET"])
def register_success():
    return "Registration successful"


@app.route("/login", methods=["GET", "POST"])
@csp_header(
    csp=csp,
)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if rm.checkPW(username, password):
            session.clear()  # Clear the old session
            session["username"] = username  # Set the new session data
            csrf_token = generate_csrf()  # Generate the CSRF token
            app_log.debug(f"CSRF token after login: {csrf_token}")
            app_log.debug(f"Session state after login: {session}")
            return redirect("/login_success", 302)
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    return render_template("login.html", form=form)


@app.route("/login_success", methods=["GET"])
def login_success():
    app_log.debug(f"Session state at /login_success: {session}")
    if "username" in session:
        return f"Login successful, welcome {session['username']}. \r\n Return to <a href='/'>Home</a>"
    return redirect("/login")


@app.route("/get-session", methods=["GET"])
@csp_header(
    csp=csp,
)
def get_session():
    app_log.debug(f"Session state at /get_session: {session}")
    if "username" in session:
        user_details = {
            "username": session["username"],
            # Add other session details if available
        }
        session_data = dict(session)  # Convert session to a dictionary
        return jsonify({"session_state": session_data, "user_details": user_details})
    return jsonify({"error": "No session found"}), 404


@app.route("/logout", methods=["GET"])
def logout():
    app_log.debug(f"Session state before logout: {session}")
    session.pop("username", None)
    app_log.debug(f"Session state after logout: {session}")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
