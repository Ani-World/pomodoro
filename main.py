import time
from datetime import datetime
from tkinter import *
import math
import mysql.connector


# ---------------------------- SQL ------------------------------- #
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="anisha20",
    database="daily_pomodoro"
)
cursor=conn.cursor()
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps=0
timer=""
start=0
timer_running = False

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, timer_running
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    heading.config(text="Timer")
    check.config(text="")
    reps = 0
    timer_running = False
    start_button.config(state=NORMAL)

# ---------------------------- Calculate time ------------------------------- #
def calculate_time():
    global start
    end=time.time()
    date_today = datetime.today().date()
    current_time = round((end - start) / 3600, 2)  # convert seconds to hours and round to 2 decimal places

    if heading.cget("text") == "Work":
        cursor.execute("select * from report where date=%s",(date_today,))
        record=cursor.fetchone()
        if record:
            time_to_add=record[1]+current_time
            cursor.execute("update report set total_duration=%s where date=%s",(time_to_add,date_today))
        else:
            cursor.execute("insert into report(date,total_duration) values(%s,%s)",(date_today,current_time))
        conn.commit()



# ---------------------------- TIMER MECHANISM ------------------------------- #
def stop_timer():
    global timer_running
    if timer_running:
        window.after_cancel(timer)  # Stop countdown
        calculate_time()  # Record only if it was a work session
        timer_running = False  # Reset flag


def start_timer():
    global reps,start,timer_running
    if timer_running:
        return

    timer_running = True
    start_button.config(state=DISABLED)
    start=time.time()
    reps+=1

    window.lift()
    window.attributes('-topmost', True)  # Temporarily force on top
    window.attributes('-topmost', False)  # Allow normal behavior
    window.focus_force()

    if reps%8==0:
        count_down(LONG_BREAK_MIN*60)
        heading.config(text="Break",fg=RED)
    elif reps%2 == 0:
        count_down(SHORT_BREAK_MIN*60)
        heading.config(text="Break", fg=PINK)
    else:
        count_down(WORK_MIN*60)
        heading.config(text="Work", fg=GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
# import  time
# time_is=5
# while time_is:
#     time.sleep(1)
#     print(time_is)
#     time_is -= 1

def count_down(count):
    count_min=math.floor(count/60)
    if count_min in range(0,10):
        count_min="0"+str(count_min)
    count_sec=count%60
    if count_sec in range(0,10):
        count_sec="0"+str(count_sec)
    canvas.itemconfig(timer_text,text=f"{count_min}:{count_sec}")
    if count>0:
        global timer
        timer=window.after(1000,count_down,count-1)
    else:
        if heading.cget("text") == "Work":
            calculate_time()
        global timer_running
        timer_running = False
        start_button.config(state=NORMAL)

        start_timer()
        marks=""
        work_sessions=math.floor(reps/2)
        for _ in range(work_sessions):
            marks+="🗸"
            check.config(text=marks)
# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Pomodoro")
window.config(padx=100,pady=50,bg=YELLOW)

canvas=Canvas(width=200,height=224,bg=YELLOW,highlightthickness=0)


tomato_img=PhotoImage(file="tomato.png")
canvas.create_image(100,112,image=tomato_img)
timer_text=canvas.create_text(100,130,text="00:00",font=(FONT_NAME,32,"bold"),fill="white")
canvas.grid(column=1,row=1)


heading=Label(text="Timer",font=(FONT_NAME,50),fg=GREEN,bg=YELLOW,highlightthickness=0)
heading.grid(column=1,row=0)

start_button=Button(text="Start",highlightthickness=0,command=start_timer)
start_button.grid(column=0,row=2)

reset_button=Button(text="Reset",highlightthickness=0,command=reset_timer)
reset_button.grid(column=2,row=2)

stop_button=Button(text="Stop",highlightthickness=0,command=stop_timer)
stop_button.grid(column=1,row=3)

check=Label(font=(FONT_NAME,20,"bold"),fg=GREEN,bg=YELLOW,highlightthickness=0)
check.grid(column=1,row=4)


window.mainloop()
