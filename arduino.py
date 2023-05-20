
import serial
import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
arduinoPort = ''

for port in ports:
    if 'CH340' in port.description:
        arduinoPort = port.device
        
arduino = serial.Serial(port = arduinoPort, baudrate = 9600, timeout = 0.1, dsrdtr = False)

def DropInColumn(col):
    if   col == 0: arduino.write(b'0')
    elif col == 1: arduino.write(b'1')
    elif col == 2: arduino.write(b'2')
    elif col == 3: arduino.write(b'3')
    elif col == 4: arduino.write(b'4')
    elif col == 5: arduino.write(b'5')
    elif col == 6: arduino.write(b'6')
    
DropInColumn(2)