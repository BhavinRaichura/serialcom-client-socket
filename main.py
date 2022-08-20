from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
from flask_socketio import SocketIO, send, emit, join_room, rooms
import serial.tools.list_ports
import time
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'socketapp'
app.config['DEBUG'] = True

socketio = SocketIO(app, cors_allowed_origins="*")


def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def findArduino(portsFound):
    commPort = ""
    newConnection = len(portsFound)

    for i in range(0, newConnection):
        port = portsFound[i]
        strPort = str(port)

        if 'Arduino' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])
            break
    return commPort


def serial_print_data(serial_port):
    output = str(random.randint(60,80)) + " " + str(random.randint(366,1956))+ " "+ str(random.randint(96,105))
    return output

@app.route('/')
def home():
    return '<h1>Home</h1>'

@app.route('/show-my-readings')
def show_my_readings():
    return render_template('connect_to_script.html')



@socketio.on('connect',namespace='/arduino')
def connect():
    print('server is connected')


@socketio.on('get_arduino_data',namespace='/arduino')
def get_arduino_data(request_arduino):
    print(request_arduino)
    ser_address = ""

    '''
    get serial ports
    chech in every 5 second serial is available or not
    
    while(ser_address ==""):
        ser_address = findArduino(get_ports())
        time.sleep(10)

        fatch data from arduino
    '''


    data_comming = serial_print_data(ser_address)

    while data_comming:
        data_comming = serial_print_data(ser_address)
        data_containor = data_comming.split(" ")
        arduino_obj = {}

        arduino_obj['Heart rate'] = data_containor[0]
        arduino_obj['Humidity'] = data_containor[1]
        arduino_obj['Temperature'] = data_containor[2]

        emit('put_arduino_data', arduino_obj, broadcast=True)
        time.sleep(2)

    print("Disconnected")
    #emit('disconnect_arduino', "disconnected form arduino", broadcast=True)


'''
@socketio.on('disconnect',namespace='/arduino')
def disconnect(msg):
    print(msg)
'''

if __name__ == "__main__":
    socketio.run(app)
