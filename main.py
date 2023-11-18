from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
# import ngrok
import pyautogui
import random
import string

# listener = ngrok.connect(5000, authtoken_from_env=True)
# print (f"Ingress established at {listener.url()}")

app = Flask(__name__)

sensitivity = 0.7

allowed_auth_tokens = []
password = "randompassword"

pyautogui.FAILSAFE = False


def generate_auth_token():
    length = 20
    allowed_auth_tokens.append(
        "".join(random.choice(string.ascii_letters) for i in range(length))
    )


@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.form
    if data["password"] == password:
        generate_auth_token()
        resp = make_response(redirect(url_for('control_page')))
        resp.set_cookie("auth_token", allowed_auth_tokens[-1])
        return resp
    else:
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
    app.run(debug=True, host="127.0.0.1", port="5002",  ssl_context="adhoc")
    # put to ngrok
