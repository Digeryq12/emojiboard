from tkinter import *
from urllib.parse import quote as urlencode
import requests
import math
import pyperclip
import os

window = Tk()

gx = 400
gy = 210
icon = PhotoImage(file=os.path.dirname(os.path.abspath(__file__)) + "\\icon.png")
window.geometry(f"{gx}x{gy}")
window.resizable(0,0)
window.title("Emoji Board")
window.iconphoto(True, icon)
current_list = []

def generate(ep):
    global current_list
    for b in current_list:
        b.place_forget()
    max_c = 9
    response = requests.get(f"https://api.emojisworld.fr/v1/{ep}").json()
    try: print("Error: " + response["message"])
    except: pass
    else: quit()
    results = response["total"]
    for r in range(1, math.ceil(results/max_c)+1):
        il = max_c
        if (results - r*max_c) < 0: il = results%max_c
        for c in range(1, il+1):
            i = (r-1)*max_c+c-1
            current_emoji = response["results"][i]["emoji"]
            btn = Button(window,
                         text=current_emoji)
            # https://claude.ai/chat/82b70a17-163b-448c-90ab-33b6360c05b9 (I always indicate the usage of any AI for my projects.)
            btn.config(width=5, height=1, command=lambda e=current_emoji: pyperclip.copy(e))
            current_list.append(btn)
            btn.place(x=10+(c-1)*40, y=50+(r-1)*25)

def search():
    e = urlencode(search_bar.get())
    if e == "": return
    generate(f"search?q={e}")

search_bar = Entry(window,
                   font=("Arial", 15))
search_button = Button(window,
                       text="Search",
                       font=("Arial", 10),
                       command=search)
refresh_button = Button(window,
                        text="Refresh",
                        font=("Arial", 10),
                        command=lambda: generate(f"random"))

search_bar.place(x=10, y=10)
search_button.place(x=240, y=10)
refresh_button.place(x=300, y=10)

generate(f"random")

window.mainloop()