import easymodbus.modbusClient

modbus_client = easymodbus.modbusClient.ModbusClient("194.94.28.231",502)
modbus_client.connect()

register_values = modbus_client.read_holdingregisters(0,3)

print("Val" + str(register_values[0]))
print("Val1" + str(register_values[1]))
print("Val2" + str(register_values[2]))

holding_registers_value = 0
holding_registers_value1 = 2
holding_registers_value2 = 3

modbus_client.write_single_register(0,holding_registers_value)
modbus_client.write_single_register(1,holding_registers_value1)
modbus_client.write_single_register(2,holding_registers_value2)

print("Val" + str(register_values[0]))
print("Val1" + str(register_values[1]))
print("Val2" + str(register_values[2]))
modbus_client.close()