import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import Menu, messagebox
import customtkinter 
import customtkinter as ctk
import time
import back_program as bp
import read_sensor as read
import read_elec as el
# from PIL import Image
# from PIL import ImageTk

app = customtkinter.CTk()
# Set the initial appearance mode
appearance_mode = "dark"
customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode(appearance_mode)



def change_color():
    status=bp.check_status()
    if status == "Worst":
        #change_color("#e51f1f")
        status_val.configure(text_color="#e51f1f")
    elif status == "Bad":
        #change_color("#f2a134")
        status_val.configure(text_color="#f2a134")
    elif status == "Warning":
        #change_color("#f7e379")
        status_val.configure(text_color="#f7e379")
    elif status == "Good":
        #change_color("#bbdb44")
        status_val.configure(text_color="#bbdb44")
    elif status == "Quality":
        #change_color("#44ce1b")
        status_val.configure(text_color="#44ce1b")
    

def update_sensorvalue():
    Temp_val.configure(text=read.get_temperature())
    EC_val.configure(text=read.get_EC())
    TDS_val.configure(text=read.get_TDS())
    pH_val.configure(text=read.get_pH())
    electricity_charge_val.configure(text=el.get_power())

    #update
    voltage_val.configure(text=":      {}".format(el.get_voltage()))
    current_val.configure(text=":      {}".format(el.get_current()))
    energy_val.configure(text=":      {}".format(el.get_energy()))
    pf_val.configure(text=":      {}".format(el.get_powerfactor()))
    status_val.configure(text=bp.check_status())

    

# Function to update the timestamp label
def update_timestamp():
    global color
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_label.configure(text=current_time)  # Use configure to update text
    update_sensorvalue()
    change_color()
    app.after(1000, update_timestamp)  # Update every 1000 milliseconds (1 second)

# Function to toggle appearance mode
def toggle_appearance_mode():
    global appearance_mode
    appearance_mode = "light" if appearance_mode == "dark" else "dark"
    customtkinter.set_appearance_mode(appearance_mode)
    img_label.configure(bg=( "#2B2B2B" if(appearance_mode == 'dark') else "#DBDBDB"))
    print(f"Switched to {appearance_mode} mode.")

def Close():
    confirm = tk.messagebox.askquestion("Exit", "Do you want to exit")
    if confirm == "yes":
        app.destroy()

def About():
    message = "     Develop by \n     65010406   Tanadon    Aunyart\n     65010426   Thanawat  Runglerdkriangkrai"
    tk.messagebox.showinfo("About Me",message)

class CustomCounter(ctk.CTkFrame):
    def __init__(self, master=None, default_value=25.0, height=255, width=340, *args, **kwargs): #170x240
        super().__init__(master, height=height, width=width, *args, **kwargs)
        self.value = default_value
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text='{:.2f}'.format(self.value),font=("Courier", 36, "bold"))
        self.label.place(x=115,y=30)

        plus_button = ctk.CTkButton(self, text=">", command=self.increment1, width=145, height=60,font=("Courier", 26, "bold"))
        plus_button.place(x=175, y=100)

        minus_button = ctk.CTkButton(self, text="<", command=self.decrement1, width=145, height=60,font=("Courier", 26, "bold"))
        minus_button.place(x=20, y=100)

        dbp_button = ctk.CTkButton(self, text=">>", command=self.increment, width=145, height=60,font=("Courier", 26, "bold"))
        dbp_button.place(x=175, y=170)

        dbm_button = ctk.CTkButton(self, text="<<", command=self.decrement, width=145, height=60,font=("Courier", 26, "bold"))
        dbm_button.place(x=20, y=170)

    def increment(self):
        self.value += 1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.Range_val,bp.stage))
        print("Increment by 1: ", self.value)

    def decrement(self):
        self.value -= 1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.Range_val,bp.stage))
        print("Decrement by 1: ", self.value)

    def increment1(self):
        self.value += 0.1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.Range_val,bp.stage))
        print("Increment by 0.1: ", self.value)

    def decrement1(self):
        self.value -= 0.1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.Range_val,bp.stage))
        print("Decrement by 0.1: ", self.value)

    def update_label(self):
        self.label.configure(text='{:.2f}'.format(self.value))

################################################################

# Create window
#app = customtkinter.CTk()
if __name__ == "__main__":  
    app.title("Chiller System")

# Set the desired width and height
locked_width = 900
locked_height = 600

# Lock the window size
app.minsize(width=locked_width, height=locked_height)
app.maxsize(width=locked_width, height=locked_height)

# Frame
frame_Menu = customtkinter.CTkFrame(master=app, height=560, width=170)
frame_Menu.place(x=20, y=20)

#Image universities logo
# usl_logo = Image.open('D:/Project/Basic_GUI/Project/Seal_of_King_Mongkut.png')
# usl_logo = usl_logo.resize((150,150))
# usl_Image = ImageTk.PhotoImage(usl_logo)
# img_label = tk.Label(master=frame_Menu,image=usl_Image,width=150,height=150,bg="#2B2B2B")
# img_label.place(x=10,y=15)

# Create a button to toggle appearance mode
toggle_button = customtkinter.CTkButton(master=frame_Menu, text="Switch Theme",font=("Aral", 16), command=toggle_appearance_mode,width=140,height=60)
toggle_button.place(relx=0.5, y=360, anchor="center")

# Create a button to exit
exit_button = customtkinter.CTkButton(master=frame_Menu, text="Close Program",font=("Aral", 16), command=Close,width=140,height=60)
exit_button.place(relx=0.5, y=510, anchor="center")

info_button = customtkinter.CTkButton(master=frame_Menu, text="About me",font=("Aral", 16), command=About,width=140,height=60)
info_button.place(relx=0.5, y=435, anchor="center")

frame_Time = customtkinter.CTkFrame(master=app, height=60, width=260)
frame_Time.place(x=210, y=20)
# Create a label to display the timestamp
timestamp_label = customtkinter.CTkLabel(master=frame_Time, text="", font=("Courier", 20, "bold"))
timestamp_label.place(relx=0.5, rely=0.5, anchor="center")

frame_electricity_charge = customtkinter.CTkFrame(master=app, height=60, width=190)
frame_electricity_charge.place(x=690,y=20)
electricity_charge_val = customtkinter.CTkLabel(master=frame_electricity_charge ,text="", font=("Courier", 22))
electricity_charge_val.place(relx=0.2,rely=0.275)
electricity_charge_label = customtkinter.CTkLabel(master=frame_electricity_charge, text="Watt", font=("Courier", 22, "bold"))
electricity_charge_label.place(relx=0.5, rely=0.275)


frame_Dashboard = customtkinter.CTkFrame(master=app, height=60, width=190)
frame_Dashboard.place(x=490, y=20)
title = customtkinter.CTkLabel(master=frame_Dashboard, text="DATA", font=("Courier", 24, "bold"))
title.place(relx=0.5, rely=0.5, anchor="center")

frame_status_display = customtkinter.CTkFrame(master=app ,height=190, width=260)#
frame_status_display.place(x=210, y=95)
status_Label = customtkinter.CTkLabel(master=frame_status_display,text="STATUS", font=("Courier", 24, "bold"))
status_Label.place(x=20, y=20)
status_val = customtkinter.CTkLabel(master=frame_status_display, font=("Courier", 36, "bold"))
status_val.place(relx=0.5, rely=0.5, anchor="center")
status = bp.check_status()

#####update
frame_Control = customtkinter.CTkFrame(master=app, height=275, width=360)## old 670
frame_Control.place(x=210, y=306)

frame_status_voltage = customtkinter.CTkFrame(master=app, height=60,width=295)
frame_status_voltage.place(x=585,y=306)
voltage_label = customtkinter.CTkLabel(master=frame_status_voltage ,text="Voltage :", font=("Courier", 20, "bold"))
voltage_label.place(relx=0.1,rely=0.3)

frame_status_current = customtkinter.CTkFrame(master=app, height=60,width=295)
frame_status_current.place(x=585,y=377)
current_label = customtkinter.CTkLabel(master=frame_status_current ,text="Current :", font=("Courier", 20, "bold"))
current_label.place(relx=0.1,rely=0.3)

frame_status_energy = customtkinter.CTkFrame(master=app, height=60,width=295)
frame_status_energy.place(x=585,y=448)
energy_label = customtkinter.CTkLabel(master=frame_status_energy ,text="Energy  :", font=("Courier", 20, "bold"))
energy_label.place(relx=0.1,rely=0.3)

frame_status_pf = customtkinter.CTkFrame(master=app, height=60,width=295)
frame_status_pf.place(x=585,y=520)
pf_label = customtkinter.CTkLabel(master=frame_status_pf ,text="PF      :", font=("Courier", 20, "bold"))
pf_label.place(relx=0.1,rely=0.3)

voltage_val = customtkinter.CTkLabel(master=frame_status_voltage ,text="", font=("Courier", 20, "bold"))
voltage_val.place(relx=0.4,rely=0.3)
current_val = customtkinter.CTkLabel(master=frame_status_current ,text="", font=("Courier", 20, "bold"))
current_val.place(relx=0.4,rely=0.3)
energy_val = customtkinter.CTkLabel(master=frame_status_energy ,text="", font=("Courier", 20, "bold"))
energy_val.place(relx=0.4,rely=0.3)
pf_val = customtkinter.CTkLabel(master=frame_status_pf ,text="", font=("Courier", 20, "bold"))
pf_val.place(relx=0.4,rely=0.3)

################################################################


counter = CustomCounter(frame_Control)
counter.pack(padx=10, pady=10)

frame_Data1 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data1.place(x=490, y=95)
Temp = customtkinter.CTkLabel(master=frame_Data1, text="Temp", font=("Courier", 22, "bold"))
Temp.place(relx=0.2, rely=0.2)
Temp_val = customtkinter.CTkLabel(master=frame_Data1 ,text="", font=("Courier", 18))
Temp_val.place(relx=0.3,rely=0.6)

frame_Data2 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data2.place(x=590, y=95)
EC = customtkinter.CTkLabel(master=frame_Data2, text="EC", font=("Courier", 22, "bold"))
EC.place(relx=0.35, rely=0.2)
EC_val = customtkinter.CTkLabel(master=frame_Data2 ,text="", font=("Courier", 18))
EC_val.place(relx=0.25,rely=0.6)

frame_Data3 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data3.place(x=690, y=95)
TDS = customtkinter.CTkLabel(master=frame_Data3, text="TDS", font=("Courier", 22, "bold"))
TDS.place(relx=0.25, rely=0.2)
TDS_val = customtkinter.CTkLabel(master=frame_Data3 ,text="", font=("Courier", 18))
TDS_val.place(relx=0.25,rely=0.6)

frame_Data4 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data4.place(x=790, y=95)
pH = customtkinter.CTkLabel(master=frame_Data4, text="pH", font=("Courier", 22, "bold"))
pH.place(relx=0.35, rely=0.2)
pH_val = customtkinter.CTkLabel(master=frame_Data4 ,text="", font=("Courier", 18))
pH_val.place(relx=0.3,rely=0.6)


# Start updating the timestamp label
update_timestamp()

# Run the main event loop
app.mainloop()
