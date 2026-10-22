from flask import Flask, jsonify, request, render_template, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "demo_http_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)


@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return render_template("index.html")


@app.route("/api/employees", methods=["POST"])
def register_employee():
    REQUEST_COUNT.labels(endpoint="/api/employees").inc()

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    department = str(data.get("department", "")).strip()
    role = str(data.get("role", "")).strip()

    if not all([name, email, department, role]):
        return jsonify(error="Please complete all fields."), 400

    if "@" not in email:
        return jsonify(error="Please enter a valid email address."), 400

    return jsonify(
        message="Employee registration successful!",
        employee={
            "name": name,
            "email": email,
            "department": department,
            "role": role
        }
    ), 201


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return jsonify(status="healthy"), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
