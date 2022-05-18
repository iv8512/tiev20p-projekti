from tkinter import *
from colours import *
import json
from PIL import ImageTk, Image
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

    def colours(self):
        for category in info_file["Colours"]:
            print(category)
            if type(info_file["Colours"][category]) == dict:
                for name, colour in info_file["Colours"][category].items():
                    print(f"  {name} {colour}")
            else:
                for colour in info_file["Colours"][category]:
                    print(f"  {colour}")
        
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
    background.config(bg=C3)
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

def create_label(frame, text, side="top", fill="both", expand=True, bg=C3):
    text, size, state = text_handler(text)
    label = Label(frame, text=text, state=state)
    label.pack(side=side, fill=fill, expand=expand)
    label.config(fg="white", bg=bg)
    label.config(font=("TkDefaultFont", size))
    return label

def create_button(frame, text, side="top", fill="both", expand=True, bg=C3):
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
    button.bind("<Enter>", lambda event: background.config(bg=C4))
    button.bind("<Leave>", lambda event: background.config(bg=C3))
    return button

def create_toggle(frame, text, side="top", fill="both", expand=True):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand)
    image_label = create_toggle_image(background, text, expand)
    # Main
    toggle = Label(background, text=text, state=state, cursor="hand2")
    toggle.pack(side="right", fill="both", expand=True)
    toggle.config(bg=C3, fg="white")
    toggle.config(height=2, font=("TkDefaultFont", size))
    toggle.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", image_label))
    # Hover effect
    toggle.bind("<Enter>", lambda event: background.config(bg=C4))
    toggle.bind("<Leave>", lambda event: background.config(bg=C3))
    return toggle

def create_toggle_image(background, text, expand, file="Toggle On.png"):
    image = image_handler(text, file)
    if expand:
        frame = create_background(background, "right", "both", False, 0, True)
        frame.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
        frame.bind("<Enter>", lambda event: background.config(bg=C4))
        frame.bind("<Leave>", lambda event: background.config(bg=C3))
    else:
        frame = background
    # Main
    label = Label(frame, image=image, cursor="hand2")
    label.pack(side="right", expand=False)
    label.config(bg=C3)
    # Binds
    label.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
    label.bind("<Enter>", lambda event: background.config(bg=C4))
    label.bind("<Leave>", lambda event: background.config(bg=C3))
    return label

def image_handler(text, file, size=40, rotation=0):
    # JL6079
    image = Image.open(file).convert("RGBA")
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    image = image.rotate(rotation)
    image = ImageTk.PhotoImage(image)
    global images
    images[text] = image
    return images[text]

def toggle_handler(text):
    global toggles
    if text not in toggles:
        toggles[text] = False
    else:
        toggles[text] = not toggles[text]
    return toggles[text]

images = {}
toggles = {}

def create_column(frame):
    column = Frame(frame, borderwidth=0)
    column.pack(side="left", fill="both", expand=True)
    column.config(bg=C2)
    return column

def create_row(frame, side="top", fill="both", expand=True, border=5, bg=C2):
    frame = Frame(frame, borderwidth=border)
    frame.pack(side=side, fill=fill, expand=expand)
    frame.config(bg=bg)
    return frame

def multiple(obj_type, amount, frame=True):
    if frame:
        frame = mainframe
    items = []
    for i in range(amount):
        items.append(obj_type(frame))
    return items

def create_square(row, i, side="top", border=5):
    frame1 = Frame(row, borderwidth=border)
    frame1.pack(side=side, fill="both", expand=True)
    frame1.config(bg=C2)
    frame2 = Frame(frame1)
    frame2.pack(side=side, fill="both", expand=True)
    frame2.config(bg=C3)
    create_label(frame2, i)

def create_mapgrid(frame):
    geometry = root.winfo_geometry()
    print(geometry)
    print(frame.winfo_width(), frame.winfo_height())
    for column_i in range(15):
        column = create_column(frame)
        for row_i in range(11):
            create_square(column, f"{column_i}/{row_i}", border=5)

"""

END

"""

mainframe = Frame(root, borderwidth=10)
mainframe.pack(side="left", fill="both", expand=True)
mainframe.config(bg=C1)

sidebar = Frame(root, width=400)
sidebar.pack(side="left", fill="both")
sidebar.config(bg=C2)
sidebar.pack_propagate(0)

def startup():
    switch_frame("Mainmenu")

def jump_point(text, toggle=False):
    match text.split():
        case ["Quit"]:
            quit()
        case ["Back"]:
            switch_frame("Mainmenu")
        case ["Toggle", *text]:
            text = " ".join(text)
            state = toggle_handler(text)
            if state:
                image = image_handler(text, "Toggle On.png")
            else:
                image = image_handler(text, "Toggle Off.png")
            toggle.configure(image=image)
        case _:
            print(text)
            switch_frame(text)

def switch_frame(frame):
    clear_frame(mainframe)
    if frame == "Mainmenu":
        switch_sidebar(frame)
    elif frame == "Play":
        create_mapgrid(mainframe)
        movement_controls()
        
    elif frame == "LVL-Selector":
        LVL_Select_scrn = create_row(mainframe, "top", "both", True, 5, C2)
        
        lvl_box = create_row(LVL_Select_scrn, "left", "both", True, 5, C3)
        create_label(lvl_box, "", "left", "x", True, C3)
        create_button(lvl_box, ("LVL-1", 20), "left", "x", False, C3)
        create_button(lvl_box, ("LVL-2", 20), "left", "x", False, C3)
        create_button(lvl_box, ("LVL-3", 20), "left", "x", False, C3)
        create_button(lvl_box, ("LVL-4", 20), "left", "x", False, C3)
        create_button(lvl_box, ("LVL-5", 20), "left", "x", False, C3)
        create_label(lvl_box, "", "left", "x", True, C3)
        
    elif frame == "Settings":
        #Settings_container = create_label(mainframe, "", "both", True, C3)
        #Settings_section1 = create_label(Settings_container, "", "both", True, C3)
        row_1, row_2 = create_row(mainframe), create_row(mainframe)
        create_label(row_1, "testtest")
        create_label(row_2, "testtest")

def switch_sidebar(frame):
    clear_frame(sidebar)
    if frame == "Mainmenu":
        create_label(sidebar, ("Pac-man", 50), "top", "x", True, C3)
        
        menu_bar = create_row(sidebar, fill="x", expand=False, bg=C3)
        create_button(menu_bar, ("Play", 20), "top", "x", True, C3)
        create_button(menu_bar, ("LVL-Selector", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Settings", 20), "top", "x", True, C3)

        create_label(sidebar, "", "top", "x", True, C2)

        Quit_border = create_row(sidebar, "bottom", "x", False, 5, C3)
        create_button(Quit_border, ("Quit", 20), "bottom", expand=False, bg=C3)

    else:
        create_label(sidebar, ("Pac-man", 50), "top", "x", True, C3)
        
        menu_bar = create_row(sidebar, fill="x", expand=False, bg=C3)
        create_button(menu_bar, ("Play", 20), "top", "x", True, C3)
        create_button(menu_bar, ("LVL-Selector", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Settings", 20), "top", "x", True, C3)

        create_label(sidebar, "", "top", "x", True, C2)

        Quit_border = create_row(sidebar, "bottom", "x", False, 5, C3)
        create_button(Quit_border, ("Back", 20), "bottom", expand=False, bg=C3)

def clear_frame(*frames):
    for frame in frames:
        for item in frame.slaves():
            item.destroy()

def movement_controls():
    global current_pos
    current_pos = [7, 5]
    change_colour(current_pos[0], current_pos[1])
    root.bind("w", lambda event: position_handler("w"))
    root.bind("a", lambda event: position_handler("a"))
    root.bind("s", lambda event: position_handler("s"))
    root.bind("d", lambda event: position_handler("d"))

def position_handler(move=""):
    if movement_validator(move):
        return
    global current_pos
    change_colour(current_pos[0], current_pos[1], False)
    if move == "w":
        current_pos[1] -= 1
    elif move == "a":
        current_pos[0] -= 1
    elif move == "s":
        current_pos[1] += 1
    elif move == "d":
        current_pos[0] += 1
    change_colour(current_pos[0], current_pos[1])
    position_label = sidebar.pack_slaves()[0]
    string = f"{current_pos[0]}/{current_pos[1]}"
    position_label.config(text=string)

def movement_validator(key):
    if key == "w":
        if current_pos[1] - 1 < 0:
            return True
    elif key == "a":
        if current_pos[0] - 1 < 0:
            return True
    elif key == "s":
        if current_pos[1] + 1 > 10:
            return True
    elif key == "d":
        if current_pos[0] + 1 > 14:
            return True

def change_colour(column, row, state=True):
    selected_column = mainframe.slaves()[column]
    # print(len(mainframe.slaves())) = 11
    item = selected_column.slaves()[row]
    if state:
        item.config(bg=C8)
    else:
        item.config(bg=C2)

root.bind("<Escape>", quit) #sys.exit
#root.iconbitmap("blume.ico")
root.title("Pac-man")
#root.geometry("1000x600+100+100")
#root.minsize(250, 200)
root.attributes('-fullscreen', True)
root.after(6, startup)
root.mainloop()
