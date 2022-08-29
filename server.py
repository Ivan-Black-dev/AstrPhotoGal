import flask, json, socket
from flask import render_template, url_for
from datetime import datetime


SERVER_IP = '127.0.0.1'
PORT = 5000


app = flask.Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', IP = SERVER_IP, PORT = PORT)


@app.route('/catalog')
def catalog():
    with open('list.txt', 'r') as f:
        names = f.read().split('\n')

    data = []
    for name in names:
        if name:
            resData = loadData(name)
            resData['date'] = convertUnixToDate(resData['date'])
            data.append(resData)

    return render_template('list.html', title='Каталог', list = data)


def loadData(name):
    with open(f'data/{name}.json', encoding="utf-8") as f:
        res = json.load(f)
    res['img'] = url_for('static', filename=f'{name}.jpg')
    return res


def convertUnixToDate(unix):
    return datetime.utcfromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    app.run('0.0.0.0')
