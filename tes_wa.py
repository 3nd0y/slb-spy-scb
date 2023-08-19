from whatsapp_api_client_python import API
import signal

def handler(signum, frame):
    print('Application closed due to ctrl-C')
    exit(1)

signal.signal(signal.SIGINT, handler)
greenAPI = API.GreenApi("1101824413", "d627598d3675458786edbe8b258a5cc3bebf58b842ad4fb8a8")
k=greenAPI.sending.sendMessage("628111466004@c.us", "hello1")
while k.data==None :
	k=greenAPI.sending.sendMessage("628111466004@c.us", "hello1")

print(k.data)
print(type(k.data))