from pymodbus.client import ModbusSerialClient
import queue

temperature=0
pH=7
calibration_fluid_EC=0
EC=0
TDS=0

update_Q=queue.Queue()

client = ModbusSerialClient(
    port="COM3",
    #port="COM8",
    timeout=2,
    baudrate=9600,
    bytesize=8,
    parity="N",
    stopbits=1
)

client.connect()

def get_temperature():
    global temperature
    return temperature

def get_pH():
    global pH
    return pH

def get_calibration():
    global calibration_fluid_EC
    return calibration_fluid_EC

def get_EC():
    global EC
    return EC

def get_TDS():
    global TDS
    return TDS

def read_data():
    global temperature
    global pH
    global EC
    global calibration_fluid_EC
    global TDS
    
    data1=client.read_holding_registers(address=0,count=3,slave=1)
    data2=client.read_holding_registers(address=0,count=3,slave=2)
    
    temp=data1.registers[0]/10
    pH_value=data1.registers[1]/10
    calibration=data2.registers[0]/10
    ec=data2.registers[1]/10
    tds=ec*0.5
    
    update_Q.put((temp,pH_value,ec,calibration,tds))
    #print(data1.registers)
    #print(data2.registers)
    
    try:
        while True:
            # Get the latest values from the queue and update the variables
            temp,pH_value,ec,calibration,tds= update_Q.get_nowait()
            temperature=temp
            pH=pH_value
            calibration_fluid_EC=calibration
            EC=ec
            TDS=tds
    except queue.Empty:
        pass
    
    


#tds (ppm)  EC (microS/cm  temperature (celcius))

