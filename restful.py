from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request  
from flask import abort
from flask import make_response

import test

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return 'Get out!🙂'

@app.route('/dachuang/api/v1/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/dachuang/api/v1/hardware')
def get_hardware():
    hardwarename = request.args.get('hardwarename')    
    unit = test.readHardware(hardwarename)
    response = {'id' : unit.id,
                'name' : unit.name,
                'status' : unit.status,
                'num' : unit.num}
    return jsonify(response)

@app.route('/dachuang/api/v1/allHardware')
def get_allHardware():
    LED = test.readHardware('redLED')
    UNIT= test.readHardware('tempUnit')
    LEDres = { 'id' : LED.id,
               'name' : LED.name,
               'status' : LED.status,
               'num' : LED.num }
    UNITres = { 'id' : UNIT.id,
                'name' : UNIT.name,
                'status' : UNIT.status,
                'num' : UNIT.num }
    return jsonify([LEDres, UNITres])

@app.route('/dachuang/api/v1/updateHardware', methods=['GET'])
def get_updateHardware():
    hardwarename = request.args.get('hardwarename')
    status = request.args.get('status')
    num = request.args.get('num')
    if status == '3':
        unit = test.readHardware(hardwarename)
        test.writeHardware(hardwarename, unit.status, num)
    else:
        test.writeHardware(hardwarename, unit.status, num)
    return jsonify({'code' : '1'})

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
