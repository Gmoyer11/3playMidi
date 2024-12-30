[Dependencies]
	Mido
	Pyserial
	ConfigParser
	
Edit the config file for your Midi port and serial port
You will likely need a loop midi driver, I suggest LoopMidi

If you don't have a name for your serial or midi port, leave the config file as is and the script will list available options

[Operation]
Once your config file is written, run the script and it will do the conversion to midi in the background. Buttons will be note on off messages. The jog wheel and T-bar are control changes on channel 1 and 2. 
If a button is not implemented, It's serial code will be printed. Two buttons pressed at the same time give a seperated code and I've only implemented some of them. Add them to the keyDict dictionary to use them.
