#import easymodbus

from easymodbus.modbusClient import ModbusClient
modbusclient = ModbusClient("194.94.86.6",502)
modbusclient.connect()
discreteInputs = modbusclient.read_discreteinputs(0, 8) #holdingregisters
print(discreteInputs)
modbusclient.close()