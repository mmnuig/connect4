
import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
arduinoPort = ''

for port in ports:
    if 'CH340' in port.description:
        arduinoPort = port.device
        
arduino = serial.Serial(port = arduinoPort, baudrate = 115200, timeout = 0.1, dsrdtr = False)