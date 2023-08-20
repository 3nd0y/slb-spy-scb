import parse_modbus as pm
from parse_modbus import get_val_modbus
from parse_modbus import get_sensor_min
import serial
import signal
import threading
import time
from whatsapp_api_client_python import API
from sys import platform

## NOTE this is for Python3, if you use for python 2.7 then will encounter payload type str which can failed in
## get_val_modbus function. Python3 serial COM will give output bytes type rather than str

hint = b'\x01\x04\x08\x58\x00\x1e\xf3\xb1'

def handler(signum, frame):
    print('Application closed due to ctrl-C')
    exit(1)


def send_wa(txt):
    greenAPI.sending.sendMessage("6281292541479@c.us", msg)

def sensor_read():
    global siteID
    global PI
    global PD
    global TI
    global TM
    comport=''
    if platform == "win32":
        comport='COM5'
    else:
        comport='/dev/ttyUSB0'
    res = []
    while(1):
        with serial.Serial(comport, 9600, timeout=1) as ser:
            payload = ser.read(16*32)
            if(len(payload)>1):
                res=get_val_modbus(get_sensor_min(payload,hint),payload)
                if len(res)!=0:
                    siteID=res[4]
                    PI=res[0]
                    PD=res[1]
                    TI=res[2]
                    TM=res[3]
                    # print("Site ID: %d\nPI: %.1f psi\nPD: %.1f psi\nTI: %.1f F\nTM: %.1f F\n\n"
                    #     %(siteID,float(PI/10),float(PD/10),float(TI/10),float(TM/10)))

##global variable
siteID = 0
PI = 0
PD = 0
TI = 0
TM = 0
greenAPI = API.GreenApi("1101824413", "d627598d3675458786edbe8b258a5cc3bebf58b842ad4fb8a8")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    x = threading.Thread(target=sensor_read)
    x.daemon = True
    x.start()
    time.sleep(60)  # waiting Poll sensor_read() get update data
    while(1):
        f = open('ampere.txt')
        wkt=time.localtime()
        print("Site ID: %d\nPI: %.1f psi\nPD: %.1f psi\nTI: %.1f F\nTM: %.1f F\n\n"
            %(siteID,float(PI/10),float(PD/10),float(TI/10),float(TM/10)))
        msg="YYA P/F - {tgl}\nYYA-1RWST - Jam {jam}\n\n*ESP Parameter\nFREQ : 54\nR/A : {amp:.1f} A\
            \nPI: {pi:.1f} psi\nPD: {pd:.1f} psi\nTI: {ti:.1f} F\nTM: {tm:.1f} F\n( Check at Uniconn Controller )\n"\
            .format(tgl=time.strftime("%d %B %Y",wkt),amp=float(f.read()),jam=time.strftime("%H:%M:%S",wkt),pi=float(PI/10),pd=float(PD/10),ti=float(TI/10),tm=float(TM/10))
        # while k.data==None :
        send_wa(msg)
        time.sleep(3600)


# print(float(f.read()))
# print(time.localtime())
