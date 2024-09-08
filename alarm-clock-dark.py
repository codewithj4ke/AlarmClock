# Project: Alarm Clock
# Application developed by: codewithj4ke - September 2024
# Learning Python programming with the assistance of AI and online courses

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import winsound
from threading import Thread
import time

# Create Object
root = Tk()
root.title("Alarm Clock")
root.geometry("500x350")
root.configure(bg="#2E2E2E")  # Dark background color

# Create a Frame for the title
title_frame = Frame(root, bg="#2E2E2E")
title_frame.pack(pady=10, anchor='n')

# Create a Frame for the input controls and layout
input_frame = Frame(root, bg="#2E2E2E")
input_frame.pack(pady=20)

# Create a Frame to hold alarm and countdown labels
info_frame = Frame(input_frame, bg="#2E2E2E")
info_frame.pack()

# Create labels for alarm time display
alarm_label = Label(info_frame, text="Set your alarm", font=("Calibri", 18), fg="#FFFFFF", bg="#2E2E2E")
alarm_label.pack(pady=(10, 0))

countdown_label = Label(info_frame, text="Countdown: --:--:--", font=("Calibri", 16), fg="#AAAAAA", bg="#2E2E2E")
countdown_label.pack(pady=(10, 0))
countdown_label.pack_forget()  # Hide countdown initially

# Create a Frame for buttons
button_frame = Frame(root, bg="#2E2E2E")
button_frame.pack(pady=10)


def update_countdown():
    """Update the countdown label with the remaining time."""
    global countdown_active
    if not countdown_active:
        countdown_label.pack_forget()
        return

    now = datetime.datetime.now()
    try:
        alarm_time = datetime.datetime.strptime(f"{hour.get()}:{minute.get()}:{second.get()}", "%H:%M:%S")
        alarm_time = now.replace(hour=alarm_time.hour, minute=alarm_time.minute, second=alarm_time.second,
                                 microsecond=0)

        if alarm_time < now:
            alarm_time += datetime.timedelta(days=1)

        remaining_time = alarm_time - now

        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        countdown_label.config(text=f"Countdown: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
    except Exception as e:
        countdown_label.config(text="Error")
        print("Error updating countdown:", e)

    root.after(1000, update_countdown)


def start_alarm_thread():
    """Start the alarm thread."""
    global alarm_thread
    alarm_thread = Thread(target=alarm)
    alarm_thread.daemon = True
    alarm_thread.start()


def alarm():
    """Run the alarm function."""
    global alarm_active
    alarm_active = True
    global countdown_active
    countdown_active = True
    while alarm_active:
        set_alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
        time.sleep(1)
        current_time = datetime.datetime.now().strftime("%H:%M:%S")

        if current_time == set_alarm_time:
            winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
            messagebox.showinfo("Alarm", "Time to Wake Up!")
            stop_alarm()
            break


def stop_alarm():
    """Stop the alarm and remove the countdown timer."""
    global alarm_active
    alarm_active = False
    global countdown_active
    countdown_active = False
    countdown_label.pack_forget()
    cancel_button.pack_forget()
    alarm_label.config(text="Alarm Triggered")

    # Show time settings again
    time_settings_frame.pack(pady=5)


def set_alarm_and_start():
    """Set the alarm and start the countdown and alarm threads."""
    global countdown_active
    countdown_active = True
    update_countdown()
    start_alarm_thread()
    countdown_label.pack()
    cancel_button.pack(side=LEFT, padx=5)
    alarm_time = f"{hour.get()}:{minute.get()}:{second.get()}"
    alarm_label.config(text=f"Alarm Set: {alarm_time}")

    # Hide time settings
    time_settings_frame.pack_forget()


def cancel_alarm():
    """Cancel the alarm and stop the countdown."""
    global alarm_active
    alarm_active = False
    global countdown_active
    countdown_active = False
    countdown_label.pack_forget()
    cancel_button.pack_forget()
    alarm_label.config(text="Alarm Cancelled")

    # Show time settings again
    time_settings_frame.pack(pady=5)


# Create the Set Alarm button and place it in the button frame
set_alarm_button = Button(button_frame, text="Set Alarm", font=("Calibri", 14), command=set_alarm_and_start,
                          bg="#4CAF50", fg="white", relief=RAISED)
set_alarm_button.pack(side=LEFT, padx=5)

# Create the Cancel Alarm button and hide it initially
cancel_button = Button(button_frame, text="Cancel Alarm", font=("Calibri", 14), command=cancel_alarm, bg="#f44336",
                       fg="white", relief=RAISED)
cancel_button.pack(side=LEFT, padx=5)

# Add Labels, Frame, Button, Comboboxes
time_settings_frame = Frame(input_frame, bg="#2E2E2E")
time_settings_frame.pack(pady=5)

Label(time_settings_frame, text="Set Time", font=("Calibri", 16), fg="#FFFFFF", bg="#2E2E2E").pack(pady=5)

hour = StringVar(root)
hours = [f'{i:02}' for i in range(24)]
hour.set(hours[0])

hour_menu = ttk.Combobox(time_settings_frame, textvariable=hour, values=hours, width=5, font=("Calibri", 14))
hour_menu.pack(side=LEFT, padx=5)

minute = StringVar(root)
minutes = [f'{i:02}' for i in range(60)]
minute.set(minutes[0])

minute_menu = ttk.Combobox(time_settings_frame, textvariable=minute, values=minutes, width=5, font=("Calibri", 14))
minute_menu.pack(side=LEFT, padx=5)

second = StringVar(root)
seconds = [f'{i:02}' for i in range(60)]
second.set(seconds[0])

second_menu = ttk.Combobox(time_settings_frame, textvariable=second, values=seconds, width=5, font=("Calibri", 14))
second_menu.pack(side=LEFT, padx=5)

# Create a Footer Frame
footer_frame = Frame(root, bg="#2E2E2E")
footer_frame.pack(side="bottom", pady=(5, 10))

# Footer label
footer_label = ttk.Label(footer_frame, text="Application developed by: codewithj4ke", font=("Calibri", 8),
                         foreground="#AAAAAA")
footer_label.pack()

# Initialize state variables
alarm_active = False
countdown_active = False

# Execute Tkinter
root.mainloop()
