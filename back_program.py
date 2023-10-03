import time
import threading
import queue

temp_tank = 30
temp_set = 25
range_val = 0.5
stage = True

# Create a queue for communication between threads
update_queue = queue.Queue()

#set stage
def set_stage(Stage):
    global stage
    if Stage==1:
        stage=True
    elif Stage==0:
        stage=False

#show temperature
def show_temperature():
    global temp_tank
    return temp_tank

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

        if temp_tank - temp_set >= range_val:
            set_stage(1)
        elif temp_tank - temp_set < 0:
            set_stage(0)

        if check_stage() == True:
            print("working")
        elif check_stage() == False:
            print("not working")
        temp_tank -= 0.1
        print(temp_tank)
        time.sleep(1)

work_thread = threading.Thread(target=work)
work_thread.daemon = True
work_thread.start()