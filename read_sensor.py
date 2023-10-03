from pymodbus.client import ModbusSerialClient
import queue

temperature=None
pH=None
EC=None

update_Q=queue.Queue()

client = ModbusSerialClient(
    port="COM3",
    timeout=2,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1
)

client.connect()


def read_data():
    global temperature
    global pH
    #global EC
    
    data1=client.read_holding_registers(address=0,count=3,slave=1)
    #data2=client2.read_holding_registers(address=0,count=3,slave=2)
    temp=data1.registers[0]/10
    pH_value=data1.registers[1]/10
    #EC=data2.registers[0]
    update_Q.put((temp,pH_value))
    print(data1.registers)
    
    try:
        while True:
            # Get the latest values from the queue and update the variables
            temp,pH_value = update_Q.get_nowait()
            temperature=temp
            pH=pH_value
    except queue.Empty:
        pass



