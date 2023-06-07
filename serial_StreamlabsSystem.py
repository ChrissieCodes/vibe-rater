import serial
import serial.tools.list_ports
import time


with serial.Serial('COM4',115200,bytesize=8,parity='N',stopbits=1, timeout=1) as ser:
    time.sleep(4)
    ser.write(b'q')
    ser.flush()




