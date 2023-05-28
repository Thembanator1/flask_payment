from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<p>Hello, World!, site was hosted</p>'

if __name__ == '__main__':
    app.run()