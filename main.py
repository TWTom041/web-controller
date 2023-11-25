from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for
import pyautogui
import random
import string
from argon2 import PasswordHasher
from flask_cors import CORS
import yt_dlp
import os
import time
import argparse

# listener = ngrok.connect(5000, authtoken_from_env=True)
# print (f"Ingress established at {listener.url()}")

app = Flask(__name__)
CORS(app)
ph = PasswordHasher()

sensitivity = 0.1
PORT = 5002
RICK_USE_BROWSER = False

allowed_auth_tokens = []
stream_url = None
expire = None

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
dirname = os.path.dirname(__file__)


def generate_auth_token():
    length = 20
    auth_token = "".join(random.choice(string.ascii_letters) for i in range(length))
    allowed_auth_tokens.append(auth_token)
    return auth_token

def update_stream_url():
    import re
    global stream_url
    global expire
    rick_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(rick_url, download=False)

    stream_url = song_info['url']
    print(stream_url)

    pattern = rf'expire=(?P<value>[^&]+)'
    result = re.search(pattern, stream_url)
    expire = int(result.group('value'))


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
        "ip": [f"https://{ip[4][0]}:{PORT}" if is_ipv4(ip[4][0]) else f"https://[{ip[4][0]}]:{PORT}" for ip in socket.getaddrinfo(socket.gethostname(), None)]
    }))
    return resp


@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.form
    with open(os.path.join(dirname, "password.txt"), "r") as f:
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
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    if request.cookies.get('auth_token', "") not in allowed_auth_tokens:
        return jsonify({"status": "error"}), 401
    if RICK_USE_BROWSER:
        import webbrowser
        webbrowser.open(url)
    else:
        if stream_url is None or expire is None or expire - time.time() < 0:
            update_stream_url()
        import vlc
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(stream_url)
        Media.get_mrl()
        player.set_media(Media)
        player.play()
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
    if not os.path.exists(os.path.join(dirname, "password.txt")):
        with open(os.path.join(dirname, "password.txt"), "w") as f:
            f.write("$argon2id$v=19$m=65536,t=3,p=4$WMVq4eniCoW8SEIHID2HzQ$DZlvFI6hnbzk0AYj142crAKhlKmyuIpCT0cinJA0sA4")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sensitivity", type=float, nargs=1, default=[0.1])
    parser.add_argument("-p", "--port", type=int, nargs=1, default=[5002])
    parser.add_argument("-rb", "--rick-use-browser", type=bool, nargs=1, default=[False])
    args = parser.parse_args()
    if args.sensitivity:
        sensitivity = args.sensitivity[0]
    if args.port:
        PORT = args.port[0]
    if args.rick_use_browser:
        RICK_USE_BROWSER = args.rick_use_browser[0]

    if os.path.exists(os.path.join(dirname, "ca-cert/ca.crt")) and os.path.exists(os.path.join(dirname, "ca-cert/ca.key")):
        context = (os.path.join(dirname, "ca-cert/ca.crt"), os.path.join(dirname, "ca-cert/ca.key"))  # or "adhoc"
    else:
        print("Warning: no certificate found, using adhoc certificate")
        context = "adhoc"
    app.run(debug=True, host="0.0.0.0", port=PORT, ssl_context=context)
