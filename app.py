from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

def send_function(config, retry=False):
    # Your function logic here
    print("Config received:", config)
    print("Retry:", retry)
    # Implement the rest of your function logic

@app.route('/submit', methods=['POST'])
def submit():
    config = request.json
    send_function(config)
    return jsonify({"status": "success"}), 200

@app.route('/')
def serve_form():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
