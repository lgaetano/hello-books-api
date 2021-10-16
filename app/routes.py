from flask import Blueprint

hello_world_bp = Blueprint("hello_world", __name__)


@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    body = "Hello, World!"
    return body


@hello_world_bp.route("/hello/JSON", methods=["GET"])
def hello_JSON():
    return {
                "name": "Ada Lovelace",
                "message": "Hello!",
                "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
            }, 200

@hello_world_bp.route("/broken-endpoint-with-broken-server-code", methods=["GET"])
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"].append(new_hobby)
    return response_body