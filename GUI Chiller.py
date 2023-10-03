import tkinter as tk
from tkinter import*
from tkinter import Menu, messagebox
import customtkinter 
import customtkinter as ctk
import time
import back_program as bp
import read_sensor
import read_elec


app = customtkinter.CTk()
# Set the initial appearance mode
appearance_mode = "dark"
customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode(appearance_mode)

# Function to update the timestamp label
def update_timestamp():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    timestamp_label.configure(text=current_time)  # Use configure to update text
    app.after(1000, update_timestamp)  # Update every 1000 milliseconds (1 second)

# Function to toggle appearance mode
def toggle_appearance_mode():
    global appearance_mode
    appearance_mode = "light" if appearance_mode == "dark" else "dark"
    customtkinter.set_appearance_mode(appearance_mode)
    print(f"Switched to {appearance_mode} mode.")

def Close():
    confirm = tk.messagebox.askquestion("Exit", "Do you want to exit")
    if confirm == "yes":
        app.destroy()

def About():
    tk.messagebox.showinfo("About Me","develop by Mr.Tanadon")

class CustomCounter(ctk.CTkFrame):
    def __init__(self, master=None, default_value=25.0, height=170, width=240, *args, **kwargs):
        super().__init__(master, height=height, width=width, *args, **kwargs)
        self.value = default_value
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text='{:.2f}'.format(self.value),font=("Arial", 24))
        self.label.place(x=90,y=20)

        plus_button = ctk.CTkButton(self, text=">", command=self.increment1, width=105, height=40)
        plus_button.place(x=125, y=70)

        minus_button = ctk.CTkButton(self, text="<", command=self.decrement1, width=105, height=40)
        minus_button.place(x=10, y=70)

        dbp_button = ctk.CTkButton(self, text=">>", command=self.increment, width=105, height=40)
        dbp_button.place(x=125, y=120)

        dbm_button = ctk.CTkButton(self, text="<<", command=self.decrement, width=105, height=40)
        dbm_button.place(x=10, y=120)

    def increment(self):
        self.value += 1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.range_val,bp.stage))
        print("Increment by 1: ", self.value)

    def decrement(self):
        self.value -= 1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.range_val,bp.stage))
        print("Decrement by 1: ", self.value)

    def increment1(self):
        self.value += 0.1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.range_val,bp.stage))
        print("Increment by 0.1: ", self.value)

    def decrement1(self):
        self.value -= 0.1
        bp.temp_set=self.value
        self.update_label()
        bp.update_queue.put((bp.temp_set,bp.range_val,bp.stage))
        print("Decrement by 0.1: ", self.value)

    def update_label(self):
        self.label.configure(text='{:.2f}'.format(self.value))

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

# Create a button to toggle appearance mode
toggle_button = customtkinter.CTkButton(master=frame_Menu, text="Switch Theme", command=toggle_appearance_mode,width=140,height=40)
toggle_button.place(relx=0.5, y=400, anchor="center")

# Create a button to exit
exit_button = customtkinter.CTkButton(master=frame_Menu, text="Close Program", command=Close,width=140,height=40)
exit_button.place(relx=0.5, y=520, anchor="center")

info_button = customtkinter.CTkButton(master=frame_Menu, text="About me", command=About,width=140,height=40)
info_button.place(relx=0.5, y=460, anchor="center")

frame_Dashboard = customtkinter.CTkFrame(master=app, height=60, width=260)
frame_Dashboard.place(x=210, y=20)
title = customtkinter.CTkLabel(master=frame_Dashboard, text="DASHBOARD", font=("Arial", 20))
title.place(relx=0.5, rely=0.5, anchor="center")

frame_Time = customtkinter.CTkFrame(master=app, height=60, width=290)
frame_Time.place(x=490, y=20)

# Create a label to display the timestamp
timestamp_label = customtkinter.CTkLabel(master=frame_Time, text="", font=("Arial", 18))
timestamp_label.place(relx=0.5, rely=0.5, anchor="center")

frame_Control = customtkinter.CTkFrame(master=app)#, height=190, width=260
frame_Control.place(x=210, y=100)

counter = CustomCounter(frame_Control)
counter.pack(padx=10, pady=10)

frame_Data1 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data1.place(x=490, y=100)
Temp = customtkinter.CTkLabel(master=frame_Data1, text="Temp", font=("Arial", 16))
Temp.place(relx=0.25, rely=0.2)

frame_Data2 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data2.place(x=590, y=100)
EC = customtkinter.CTkLabel(master=frame_Data2, text="EC", font=("Arial", 16))
EC.place(relx=0.35, rely=0.2)

frame_Data3 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data3.place(x=690, y=100)
TDS = customtkinter.CTkLabel(master=frame_Data3, text="TDS", font=("Arial", 16))
TDS.place(relx=0.3, rely=0.2)

frame_Data4 = customtkinter.CTkFrame(master=app, height=190, width=90)
frame_Data4.place(x=790, y=100)
pH = customtkinter.CTkLabel(master=frame_Data4, text="pH", font=("Arial", 16))
pH.place(relx=0.35, rely=0.2)

frame_Graph = customtkinter.CTkFrame(master=app, height=265, width=670)
frame_Graph.place(x=210, y=316)

# Start updating the timestamp label
update_timestamp()

# Run the main event loop
app.mainloop()
