# app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Projeto Rodando!</h1>'

if __name__ == '__main__':
    app.run(port=5000, debug=True)