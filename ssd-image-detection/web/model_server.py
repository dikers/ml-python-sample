from flask import Flask, request
import json

app = Flask(__name__)


@app.route('/')
def hello_world():

    print(request.args.__str__())
    return 'Hello World!'

@app.route('/data')
def get_data():
    s = ['张三', '年龄', '姓名']
    t = dict()
    t['data'] = s
    return json.dumps(t, ensure_ascii=False)



if __name__ == '__main__':
    app.run()