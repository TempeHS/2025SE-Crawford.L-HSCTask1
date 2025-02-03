from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import post_manager as pm
import register_manager as rm

api_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)

api_key = "sj5oJhfS9YoJHo0aOFSEjGYnboe6yPoF"

api = Flask(__name__)
api.secret_key = r"nEksrUMh4vnYXa9I52U7uUs4TX2mA1yk"  # Ensure you have a secret key for session management
CORS(api)
limiter = Limiter(
    app=api,
    key_func=get_remote_address,
    default_limits=["1 per second", "15 per minute"],
    storage_uri="memory://",
)


@api.before_request
def log_request_info():
    logging.debug(f"Request Headers: {request.headers}")
    logging.debug(f"Request Body: {request.get_data()}")


def login_required(f):
    def wrap(*args, **kwargs):
        if "username" not in session:
            return unauthorized_error("Unauthorized access")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def require_api_key(f):
    def wrap(*args, **kwargs):
        if request.headers.get("x-api-key") != api_key:
            return unauthorized_error("Unauthorized access")
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap


def get_request_data():
    if request.content_type == "application/json":
        return request.get_json()
    elif request.content_type == "application/x-www-form-urlencoded":
        return request.form.to_dict()
    else:
        return {}


@api.errorhandler(401)
def unauthorized_error(error):
    return jsonify({"error": "Unauthorized Access!"}), 401


@api.route("/api", methods=["POST"])
@require_api_key
def get_data():
    data = get_request_data()
    logging.info(f"Received data: {data}")
    return jsonify(data)


@api.route("/all-posts", methods=["POST"])
@require_api_key
# @login_required
def get_all_posts():
    return jsonify({"posts": "All posts"}), 200


@api.route("/add-post", methods=["POST"])
@require_api_key
# @login_required
def add_post():
    data = get_request_data()
    logging.info(f"Received data: {data}")
    return jsonify(data), 201


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=4000)
