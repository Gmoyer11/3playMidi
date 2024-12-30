import serial
import serial.tools.list_ports
import mido
import configparser
import os 
from time import sleep

path = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(path+'\config.txt')

serialPort = config['DEFAULT'].get('serialPort')
midiName = config['DEFAULT'].get('midiName')
keydict = {
	"10FF":"0",
	"11FF":"0",
	"12FF":"0",
	"13FF":"0",
	"10FE":"1",
	"10FD":"2",
	"10FB":"3",
	"10FC":"3",
	"10FA":"3",
	"10F9":"3",
	"10F7":"4",
	"10DF":"5",
	"10EF":"6",
	"10BF":"7",
	"11FE":"8",
	"11EF":"9",
	"11FD":"10",
	"11DF":"11",
	"11FB":"12",
	"11BF":"13",
	"11F7":"14",
	"13FE":"15",
	"13FD":"16",
	"13FB":"17",
	"13F7":"18",
	"13EF":"19",
	"12F7":"20",
	"12EF":"21",
	"12DF":"22",
	"12BF":"23",
	"127F":"24",
	"13DF":"25",
	"13BF":"26",
	"137F":"27",
	"12FE":"28",
	"12FD":"29",
	"12FB":"30",
	"139F":"33",
	"135F":"34",
	"12F6":"35",
	"12BE":"36",
	"12DE":"31"

}
prevJog = 0
prevkey = 0

#main program logic
print("[Reading Config]")
print("Serial Port: "+serialPort)
print("Midi Device: "+midiName)

#Initialize serial port for controller
try:
    controller = serial.Serial(serialPort)
except:	
    #Print available port names if unsucessful
    portNames = ''
    for port in serial.tools.list_ports.comports():
        portNames = portNames + port.name + ' '
    print('Serial Port Error, Available Ports: ', portNames)
    quit()

#Initialize Midi port
try:
    midiOut = mido.open_output(midiName)
except:
    print('Midi Device Error, Available Ports: ',mido.get_output_names())
    quit()

#Main Program Loop

print("[Starting Loop]")
while(True):
	#Error handing for the controller getting unplugged
	try:
		byte = controller.read(5).decode('utf-8')[:4]
	except serial.SerialException:
		print("Controller Lost, Retrying")
		sleep(1)
		try:
			controller.close()
			controller = serial.Serial(serialPort)
		except:
			continue
				
	#Control Change for Tee Bar
	if byte[:2] == "80":
		teeBar = int(int("0x"+byte[2:], 0)/2)
		msg = mido.Message('control_change', control=1, value=teeBar)
		midiOut.send(msg)
		continue

	#Control Change for Jog Wheel
	if byte[:2] == "96":
		jogPosition = int("0x"+byte[2:],0)
		#jogWheel = int(int("0x"+byte[2:], 0)/2)
		#msg = mido.Message('control_change', control=2, value=jogWheel)
		#midiOut.send(msg)
		#continue
		if jogPosition > prevJog or jogPosition == 0:
			msg = mido.Message('control_change', control=2, value=65)
			midiOut.send(msg)
		else:
			if jogPosition < prevJog or jogPosition == 255:
				msg = mido.Message('control_change', control=2, value=63)
				midiOut.send(msg)
		prevJog = jogPosition
		continue
	
	#Message for all other keys
	keybyte =  keydict.get(byte)
	if keybyte:
		keybyte = int(keybyte)
		if keybyte != 0:
			prevKey = keybyte
			msg = mido.Message('note_on', note=keybyte)
			midiOut.send(msg)
		else:
			msg = mido.Message('note_off', note=prevKey)
			midiOut.send(msg)
	else:
		print(byte)
