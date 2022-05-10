from tkinter import *
import json
#from interactables import *

root = Tk()

with open("info.json") as data:
    info_file = json.load(data)

class InfoClass:
    
    def __init__(self):
        self.background = self.text_handler("background")
        self.label = self.text_handler("label")
        self.button = self.text_handler("button")
        self.toggle = self.text_handler("toggle")
        self.info = self.text_handler("info")
        
    def text_handler(self, item):
        text = info_file["InfoClass"][item]
        if ":" in text:
            for marker in text.split(":"):
                if marker in info_file["InfoClass"]:
                    text = text.replace(f":{marker}:", info_file["InfoClass"][marker])
                else:
                    pass
        return text
        
info = InfoClass()

"""

START

"""

def create_background(frame, side, fill, expand, border=5, cursor=False):
    if cursor:
        background = Frame(frame, borderwidth=border, cursor="hand2")
    else:
        background = Frame(frame, borderwidth=border)
    background.pack(side=side, fill=fill, expand=expand)
    background.config(bg="#323233")
    return background

def text_handler(text):
    #JL6079
    """
    checks if ´text´is tuple
    checks how many items are in ´text´
    """
    #Two items
    if type(text) == tuple and len(text) == 2:
        #checks if 2nd item is an integer
        if type(text[1]) == int:
            text, size, state = text[0], text[1], NORMAL
        else:
            text, size, state = text[0], 10, text[1]
    #Three items
    elif type(text) == tuple and len(text) == 3:
        text, size, state = text[0], text[1], text[2]
    #One iem    
    else:
        text, size, state = text, 10, NORMAL
    return text, size, state

def create_label(frame, text, fill="both", expand=True, bg="#323233"):
    text, size, state = text_handler(text)
    label = Label(frame, text=text, state=state)
    label.pack(side="top", fill=fill, expand=expand)
    label.config(fg="white", bg=bg)
    label.config(font=("TkDefaultFont", size))
    return label

def create_button(frame, text, side="top", fill="both", expand=True, bg="#323233"):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand)
    # Main
    button = Label(background, text=text, state=state, cursor="hand2")
    button.pack(side=side, fill="both", expand=True)
    button.config(bg=bg, fg="white")
    button.config(height=2, font=("TkDefaultFont", size))
    button.bind("<Button-1>", lambda event: jump_point(text))
    # Hover effect
    button.bind("<Enter>", lambda event: background.config(bg="#575759"))
    button.bind("<Leave>", lambda event: background.config(bg="#323233"))
    return button

def create_toggle(frame, text, side="top", fill="both", expand=True):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand)
    image_label = create_toggle_image(background, text, expand)
    # Main
    toggle = Label(background, text=text, state=state, cursor="hand2")
    toggle.pack(side="right", fill="both", expand=True)
    toggle.config(bg="#323233", fg="white")
    toggle.config(height=2, font=("TkDefaultFont", size))
    toggle.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", image_label))
    # Hover effect
    toggle.bind("<Enter>", lambda event: background.config(bg="#575759"))
    toggle.bind("<Leave>", lambda event: background.config(bg="#323233"))
    return toggle

def create_toggle_image(background, text, expand, file="Toggle On.png"):
    images = image_handler(text, file)
    if expand:
        frame = create_background(background, "right", "both", False, 0, True)
        frame.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
        frame.bind("<Enter>", lambda event: background.config(bg="#575759"))
        frame.bind("<Leave>", lambda event: background.config(bg="#323233"))
    else:
        frame = background
    # Main
    label = Label(frame, image=images[text], cursor="hand2")
    label.pack(side="right", expand=False)
    label.config(bg="#323233")
    # Binds
    label.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
    label.bind("<Enter>", lambda event: background.config(bg="#575759"))
    label.bind("<Leave>", lambda event: background.config(bg="#323233"))
    return label

def image_handler(text, file):
    image = get_image(file)
    global images
    images[text] = image
    return images

def get_image(file):
    img = Image.open(file).convert("RGBA")
    img = img.resize((40, 40), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img

def toggle_handler(text):
    global toggles
    if text not in toggles:
        toggles[text] = False
    else:
        toggles[text] = not toggles[text]
    return toggles[text]

images = {}
toggles = {}

"""

END

"""

mainframe = Frame(root)
mainframe.pack(side="top", fill="both", expand=True)
mainframe.config(bg="#1B1B1B")


def jump_point(text):
    match text.split():
        case ["temp"]:
            pass
        case _:
            print(text)
            switch_frame(text)

def switch_frame(frame):
    clear_frame()
    if frame == "Mainmenu":
        pass
        
    elif frame == "Play":
        create_label(mainframe, ("test"))
        
    elif frame == "LVL-Selector":
        create_label(mainframe, ("", 100), "y", True, "#1b1b1b")
        lvl_padding = create_label(mainframe, "", "y", False)
        lvl_box = create_label(lvl_padding, ("", 100), "x", True, "#1b1b1b")
        create_button(lvl_box, ("LVL-1", 20), "left", "x", False, "#252526")
        create_button(lvl_box, ("LVL-2", 20), "left", "x", False, "#252526")
        create_button(lvl_box, ("LVL-3", 20), "left", "x", False, "#252526")
        create_button(lvl_box, ("LVL-4", 20), "left", "x", False, "#252526")
        create_button(lvl_box, ("LVL-5", 20), "left", "x", False, "#252526")
        create_label(mainframe, ("", 100), "y", True, "#1b1b1b")
        
    elif frame == "Settings":
        create_label(mainframe, "settings")

def switch_sidebar(frame):
        padding = create_label(mainframe, "", "x", True)
        create_label(padding, "", "none", True)
        create_label(padding, ("Pac-man", 50), "none", True)
        create_label(padding, "", "none", True)
        menubar = create_label(mainframe, "test", "x", expand=True)
        create_button(menubar, ("Play", 20), "left", "x", True)
        create_button(menubar, ("LVL-Selector", 20), "left", "x", True)
        create_button(menubar, ("Settings", 20), "left", "x", True)        

def clear_frame():
    for item in mainframe.slaves():
        item.destroy()

switch_frame("Mainmenu")

root.title("Pac-man")
root.geometry("1000x600+100+100")
root.minsize(250, 200)
root.mainloop()
