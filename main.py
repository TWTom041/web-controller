from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
import pyautogui
import random
import string
from argon2 import PasswordHasher
from flask_cors import CORS

# listener = ngrok.connect(5000, authtoken_from_env=True)
# print (f"Ingress established at {listener.url()}")

app = Flask(__name__)
CORS(app)
ph = PasswordHasher()

sensitivity = 0.1
port = 5002

allowed_auth_tokens = []

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


def generate_auth_token():
    length = 20
    auth_token = "".join(random.choice(string.ascii_letters) for i in range(length))
    allowed_auth_tokens.append(auth_token)
    return auth_token


@app.route("/api/lan_ip", methods=["GET"])
def lan_ip():
    import socket
    def is_ipv4(ip):
        import ipaddress
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    resp = make_response(jsonify({
        "ip": [f"https://{ip[4][0]}:{port}" if is_ipv4(ip[4][0]) else f"https://[{ip[4][0]}]:{port}" for ip in socket.getaddrinfo(socket.gethostname(), None)]
    }))
    return resp


@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.form
    with open("password.txt", "r") as f:
        password_hashed = f.read()
    try:
        ph.verify(password_hashed, data["password"])
        auth_token = generate_auth_token()
        resp = make_response(redirect(url_for('control_page')))
        resp.set_cookie("auth_token", auth_token)
        return resp
    except:
        return jsonify({"status": "error"})


@app.route("/api/mouse", methods=["POST"])
def mouse():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    pyautogui.moveRel(data["x"] * sensitivity, data["y"] * sensitivity, duration=30 / 1000)
    return jsonify({"status": "ok"})


@app.route("/api/scroll", methods=["POST"])
def scroll():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    pyautogui.scroll(data["amount"])
    return jsonify({"status": "ok"})


@app.route("/api/click", methods=["POST"])
def click():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    if data["updown"] == "up":
        pyautogui.mouseUp(button=data["button"])
    elif data["updown"] == "down":
        pyautogui.mouseDown(button=data["button"])
    return jsonify({"status": "ok"})


@app.route("/api/keyboard", methods=["POST"])
def keyboard():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    data = request.get_json()
    updown = data["updown"]
    if updown == "up":
        pyautogui.keyUp(data["key"])
    elif updown == "down":
        pyautogui.keyDown(data["key"])
    return jsonify({"status": "ok"})

@app.route("/api/rickroll", methods=["POST"])
def rickroll():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    import webbrowser
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return jsonify({"status": "ok"})


@app.route("/control_page", methods=["GET"])
def control_page():
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return redirect(url_for('login_page'))

    return render_template("control_page.html")


@app.route("/login_page", methods=["GET"])
def login_page():
    return render_template("login_page.html")


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login_page"))


if __name__ == "__main__":
    context = ("ca-cert/ca.crt", "ca-cert/ca.key")  # or "adhoc"
    app.run(debug=True, host="0.0.0.0", port=port, ssl_context=context)
    # put to ngrok
