import json

with open("settings.json") as data:
    settings = json.load(data)

C1 = settings["Colours"]["Current"]["C1"]
C2 = settings["Colours"]["Current"]["C2"]
C3 = settings["Colours"]["Current"]["C3"]
C4 = settings["Colours"]["Current"]["C4"]

D1 = settings["Colours"]["Default"]["D1"]
D2 = settings["Colours"]["Default"]["D2"]
D3 = settings["Colours"]["Default"]["D3"]
D4 = settings["Colours"]["Default"]["D4"]

TEST = "hmmhmm"

if __name__ == '__main__':

    from tkinter import *

    root= Tk()

    def create_label(frame, text, bg="#323233"):
        label = Label(frame, text=text)
        label.pack(side="top", fill="both", expand=True)
        label.config(fg="white", bg=bg)
        label.config(font=("TkDefaultFont", 10))

    left = Frame(root)
    left.pack(side="left", fill="both", expand=True)
    right = Frame(root)
    right.pack(side="left", fill="both", expand=True)

    with open("settings.json") as data:
        data = json.load(data)

    # Default Colours
    for name, colour in data["Colours"]["Default"].items():
        print(name, colour)
        create_label(left, f"{name} {colour}", colour)

    # Current Colours
    for name, colour in data["Colours"]["Current"].items():
        print(name, colour)
        create_label(right, f"{name} {colour}", colour)

    root.bind("<Escape>", quit) #sys.exit
    #root.iconbitmap("blume.ico")
    root.title("Colours")
    root.geometry("600x400")
    root.mainloop()
