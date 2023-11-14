from flask import Flask, request, jsonify, render_template
# import ngrok
import pyautogui

# listener = ngrok.connect(5000, authtoken_from_env=True)
# print (f"Ingress established at {listener.url()}")

app = Flask(__name__)

@app.route('/api/mouse', methods=['POST'])
def mouse():
    data = request.get_json()
    pyautogui.moveTo(data['x'], data['y'])
    return jsonify({'status': 'ok'})

@app.route('/api/scroll', methods=['POST'])
def scroll():
    data = request.get_json()
    pyautogui.scroll(data['amount'])
    return jsonify({'status': 'ok'})

@app.route('/api/keyboard', methods=['POST'])
def keyboard():
    data = request.get_json()
    print(data)
    updown = data['updown']
    if updown == 'up':
        print(data["key"], "up")
        pyautogui.keyUp(data['key'])
    elif updown == 'down':
        print(data["key"], "down")
        pyautogui.keyDown(data['key'])
    return jsonify({'status': 'ok'})

@app.route('/control_page', methods=['GET'])
def control_page():
    return render_template('control_page.html')

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port="5000")
    # put to ngrok

