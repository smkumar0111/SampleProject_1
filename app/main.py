"""Simple Flask application used as a Jenkins CI/CD sample project.

This app deliberately has:
  - no external network calls
  - no user data collection
  - no dynamic code execution (no eval/exec)
  - no hardcoded secrets or credentials

It exists purely to give a Jenkins pipeline something real to
checkout, install, lint, test, and security-scan.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    """Basic health check endpoint."""
    return jsonify(status="ok"), 200


@app.route("/add", methods=["GET"])
def add():
    """Add two numbers passed as query parameters `a` and `b`."""
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
    except ValueError:
        return jsonify(error="a and b must be numbers"), 400
    return jsonify(result=a + b), 200


if __name__ == "__main__":
    # Bound to localhost on purpose (avoids Bandit B104 "binding to all interfaces")
    app.run(host="127.0.0.1", port=5000)
