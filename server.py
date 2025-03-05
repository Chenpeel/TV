from flask import Flask, send_file

app = Flask(__name__)

@app.route('/combined.m3u')
def serve_m3u():
    return send_file('combined.m3u', mimetype='audio/x-mpegurl')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
