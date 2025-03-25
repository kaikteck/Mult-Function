from flask import Flask, jsonify, request, render_template
import json
import speedtest
import time
import os

app = Flask(__name__)

# Ensure the imcss directory exists
if not os.path.exists('static/img'):
    os.makedirs('static/img')

def format_speed(speed_bps):
    speed_mbps = speed_bps / 1_000_000  # Convert to Mbps
    if speed_mbps >= 1:
        return f"{speed_mbps:.1f} Mbps"
    else:
        speed_kbps = speed_bps / 1_000  # Convert to Kbps
        return f"{speed_kbps:.1f} Kbps"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_tasks')
def get_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({'tasks': []})

@app.route('/save_tasks', methods=['POST'])
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(request.json, f)
    return jsonify({'status': 'success'})

@app.route('/speed_test')
def speed_test():
    try:
        st = speedtest.Speedtest()
        print("Finding best server...")
        st.get_best_server()
        
        print("Testing download speed...")
        download_speed = st.download()
        download_formatted = format_speed(download_speed)
        
        print("Testing upload speed...")
        upload_speed = st.upload()
        upload_formatted = format_speed(upload_speed)
        
        print("Getting ping...")
        ping = st.results.ping
        
        return jsonify({
            'download': download_formatted,
            'upload': upload_formatted,
            'ping': round(ping)
        })
    except Exception as e:
        print(f"Error during speed test: {str(e)}")
        return jsonify({
            'error': 'Erro ao realizar o teste. Por favor, tente novamente.'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
