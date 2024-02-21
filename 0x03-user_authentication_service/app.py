#!/usr/bin/env python3
"""Flask Application."""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index():
    """
    Handle GET requests to the root URL ("/").

    Returns:
        Response: A JSON response containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
