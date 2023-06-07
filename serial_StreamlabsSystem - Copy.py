import serial
import serial.tools.list_ports
import time

ScriptName = "Serial"
Website = "chrissiecodes.com"
Description = "starts bubble machine"
Creator = "Chrissie"
Version = "1.0.0"

def Init():
    return

def Execute(data):
    if data.GetParam(0) != "!serial":
        with serial.Serial('COM4',115200,bytesize=8,parity='N',stopbits=1, timeout=1) as ser:
            time.sleep(4)
            ser.write(b'q')
            ser.flush()

def Tick():
    return



