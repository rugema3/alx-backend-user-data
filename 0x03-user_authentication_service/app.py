#!/usr/bin/env python3
"""Flask Application."""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    Handle GET requests to the root URL ("/").

    Returns:
        Response: A JSON response containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_user():
    """
    Handle POST requests to /users to register a new user.

    Expects form data fields: "email" and "password".

    Returns:
        Response: A JSON response indicating success or failure.
    """

    try:
        email = request.form.get("email")
        password = request.form.get("password")

        # Attempt to register the user
        user = AUTH.register_user(email, password)

        # Return success response
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError as e:
        # Return error response if user already exists
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
