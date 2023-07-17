import math
from tkinter import *
from tkinter import messagebox, ttk
from ttkthemes import themed_tk as tk
from ttkthemes import ThemedStyle

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
REPS = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset():
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    label_timer.config(text="Timer")
    text_checkmark.config(text="")
    global REPS
    REPS = 0
    work_dropdown.config(state="normal")
    break_dropdown.config(state="normal")
    long_break_dropdown.config(state="normal")
    start_button.state(["!disabled"])
    reset_button.state(["disabled"])

def validate_and_start():
    work_time_value = work_dropdown.get()
    break_time_value = break_dropdown.get()
    long_break_time_value = long_break_dropdown.get()

    if work_time_value == "Select" or break_time_value == "Select" or long_break_time_value == "Select":
        messagebox.showerror("Invalid Input", "Please select values for all durations.")
        return

    start_button.state(["disabled"])
    work_dropdown.config(state="disabled")
    break_dropdown.config(state="disabled")
    long_break_dropdown.config(state="disabled")
    reset_button.state(["!disabled"])

    start_timer()

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global REPS
    REPS += 1
    work_seconds = int(work_dropdown.get()) * 60
    short_break_seconds = int(break_dropdown.get()) * 60
    long_break_seconds = int(long_break_dropdown.get()) * 60

    if REPS % 8 == 0:
        label_timer.config(text="Long Break", font=(FONT_NAME, 45, "bold"), fg=RED, bg=YELLOW)
        count_down(long_break_seconds)
    elif REPS % 2 == 0:
        label_timer.config(text="Short Break", font=(FONT_NAME, 45, "bold"), fg=PINK, bg=YELLOW)
        count_down(short_break_seconds)
    else:
        label_timer.config(text="Work", font=(FONT_NAME, 45, "bold"), fg=GREEN, bg=YELLOW)
        count_down(work_seconds)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    count_min = math.floor(count / 60)
    count_seconds = count % 60
    if count_seconds < 10:
        count_seconds = f"0{count_seconds}"

    if count_min < 10:
        count_min = f"0{count_min}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_seconds}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(REPS / 2)
        for _ in range(work_sessions):
            marks += "✔"
        text_checkmark.config(text=marks, font=(FONT_NAME, 25, "bold"), bg=YELLOW, fg=GREEN)

# ---------------------------- UI SETUP ------------------------------- #
window = tk.ThemedTk()
window.get_themes()
window.set_theme("arc")

window.title("Pomodoro Clock")
window.config(padx=50, pady=50, bg=YELLOW)
style = ThemedStyle(window)
style.configure("TButton", font=(FONT_NAME, 12, "bold"), background=YELLOW, width=10)

canvas = Canvas(window, width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=("Courier", 35, "bold"))
canvas.grid(column=0, row=0, columnspan=2, pady=20)

label_timer = Label(window, text="Timer", font=(FONT_NAME, 45, "bold"), fg=GREEN, bg=YELLOW)
label_timer.grid(column=0, row=1, columnspan=2, pady=10)

work_label = Label(window, text="Work Time (mins):", font=(FONT_NAME, 12, "bold"), fg=GREEN, bg=YELLOW)
work_label.grid(column=0, row=2, sticky="e", padx=(0, 10))
work_dropdown = ttk.Combobox(window, values=["Select", 10, 20, 30, 40, 50, 60], state="readonly")
work_dropdown.current(0)
work_dropdown.grid(column=1, row=2, sticky="w")

break_label = Label(window, text="Break Time (mins):", font=(FONT_NAME, 12, "bold"), fg=PINK, bg=YELLOW)
break_label.grid(column=0, row=3, sticky="e", padx=(0, 10))
break_dropdown = ttk.Combobox(window, values=["Select", 5, 10, 15, 20, 25, 30], state="readonly")
break_dropdown.current(0)
break_dropdown.grid(column=1, row=3, sticky="w")

long_break_label = Label(window, text="Long Break Time (mins):", font=(FONT_NAME, 12, "bold"), fg=RED, bg=YELLOW)
long_break_label.grid(column=0, row=4, sticky="e", padx=(0, 10))
long_break_dropdown = ttk.Combobox(window, values=["Select", 15, 20, 25, 30, 35, 40], state="readonly")
long_break_dropdown.current(0)
long_break_dropdown.grid(column=1, row=4, sticky="w")

start_button = ttk.Button(window, text="Start", command=validate_and_start)
start_button.grid(column=0, row=5, pady=10, sticky="e")

reset_button = ttk.Button(window, text="Reset", state="disabled", command=reset)
reset_button.grid(column=1, row=5, pady=10, sticky="w")

text_checkmark = Label(window, font=(FONT_NAME, 25, "bold"), bg=YELLOW, fg=GREEN)
text_checkmark.grid(column=0, row=6, columnspan=2, pady=10)

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(6, weight=1)

window.mainloop()

