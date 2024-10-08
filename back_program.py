import time
import threading
import queue
import read_sensor as sensor
import read_elec as Electric
import sent_nodered as Nodered

temp_tank = None
temp_set = 25
Range_val = 0.5
stage = True
ST=""

# Create a queue for communication between threads
update_queue = queue.Queue()

#set stage
def set_stage(Stage):
    global stage
    if Stage==1:
        stage=True
    elif Stage==0:
        stage=False
        
#show range
def show_range():
    global range
    return range

#check working state
def check_stage():
    global stage
    if stage:
        return True
    else:
        return False
    
def check_status():
    count=0
    global ST
    status=["Worst","Bad","Warning","Good","Quality"]
    if sensor.get_EC()<100:
        count+=1
    if sensor.get_TDS()<100:
        count+=1
    if sensor.get_pH()<5 and sensor.get_pH()>10:
        count+=1
    if sensor.get_temperature()>28 and sensor.get_temperature()<22:
        count+=1
    ST=status[count]
    return status[count]
    


def work():
    global stage
    global temp_tank
    global temp_set
    global range_val

    while True:
        # Check if there are updates in the queue
        try:
            while True:
                # Get the latest values from the queue and update the variables
                temp_value, range_value, stage_value = update_queue.get_nowait()
                temp_set = temp_value
                range_val = range_value
                stage = stage_value
        except queue.Empty:
            pass
        sensor.read_data()
        Electric.electric_data()
        Nodered.sent_data_to_nodered()
        
        #print(Electric.Voltage)
        #print(Electric.Current)
        #print(Electric.Power)
        #print(sensor.get_TDS())
        #print(sensor.get_EC())
        #print(sensor.get_pH())
        #print(sensor.get_temperature())
        
        temp_tank=sensor.temperature
        if temp_tank - temp_set >= Range_val:
            set_stage(1)
        elif temp_tank - temp_set < 0:
            set_stage(0)

        if check_stage() == True:
            print("working")
        elif check_stage() == False:
            print("not working")
        time.sleep(1)

work_thread = threading.Thread(target=work)
work_thread.daemon = True
work_thread.start()