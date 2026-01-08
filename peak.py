from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Peak App is Running!</h1><p>Deployment successful.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
