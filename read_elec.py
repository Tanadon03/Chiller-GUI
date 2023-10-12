import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import queue

Voltage=0
Current=0
Power=0
Energy=0
Frequency=0
PF=0

Q=queue.Queue()

ser = serial.Serial(
        #port='COM4',
        port='COM5',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=0
    )

master = modbus_rtu.RtuMaster(ser)
master.set_timeout(2.0)
master.set_verbose(True)

def get_voltage():
    global Voltage
    return Voltage

def get_current():
    global Current
    return Current

def get_power():
    global Power
    return Power

def get_energy():
    global Energy
    return Energy

def get_frequency():
    global Frequency
    return Frequency

def get_powerfactor():
    global PF
    return PF

def electric_data():
    global Voltage
    global Current
    global Power
    global Energy
    global Frequency
    global PF
    try:
            data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
            voltage = data[0] / 10.0  # [V]
            current = (data[1] + (data[2] << 16)) / 1000.0  # [A]
            power = (data[3] + (data[4] << 16)) / 10.0  # [W]
            energy = data[5] + (data[6] << 16)  # [Wh]
            frequency = data[7] / 10.0  # [Hz]
            powerFactor = data[8] / 100.0
            
            #print(data)
            Q.put((voltage,current,power,energy,frequency,powerFactor))
            
            try:
                while True:
                    voltage,current,power,energy,frequency,powerFactor=Q.get_nowait()
                    Voltage=voltage
                    Current=current
                    Power=power
                    Energy=energy
                    Frequency=frequency
                    PF=powerFactor       
            except queue.Empty:
                pass
            
    except Exception as e:
            print(f"Error: {e}")



    

