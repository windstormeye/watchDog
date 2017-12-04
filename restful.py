from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request  
from flask import abort
from flask import make_response

import test

app = Flask(__name__)
api = Api(app)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/')
def index():
    return 'Get out!🙂'

@app.route('/dachuang/api/v1/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/dachuang/api/v1/hardware')
def get_hardware():
    hardwarename = request.args.get('hardwarename')
    unit = test.readHardware(hardwarename, 0)
    response = {'id' : unit.id,
                'name' : unit.name,
                'status' : unit.status,
                'num' : unit.num}
    return jsonify(response)

@app.route('/dachuang/api/v1/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    isID = 0
    for taskUnit in tasks:
        if taskUnit['id'] == task_id:
            isID = 1
            return jsonify({'task':taskUnit})
    if isID == 0:
        abort(404);
    else:
        return unit;

@app.errorhandler(404)
def no_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
