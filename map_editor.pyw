from tkinter import *
from colours import *
import json, math, os
#from interactables import *

root = Tk()

sidebar = Frame(root, width=400)
sidebar.pack(side="left", fill="both")
sidebar.config(bg=C2)
sidebar.pack_propagate(0)

mainframe = Frame(root, borderwidth=10)
mainframe.pack(side="left", fill="both", expand=True)
mainframe.config(bg=C1)

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

def create_background(frame, side, fill, expand, bg, border=5, cursor=False):
    if cursor:
        background = Frame(frame, borderwidth=border, cursor="hand2")
    else:
        background = Frame(frame, borderwidth=border)
    background.pack(side=side, fill=fill, expand=expand)
    background.config(bg=bg)
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

def create_label(frame, text, side="top", fill="both", expand=True, bg=C3, fg="white"):
    text, size, state = text_handler(text)
    label = Label(frame, text=text, state=state)
    label.pack(side=side, fill=fill, expand=expand)
    label.config(fg=fg, bg=bg)
    label.config(font=("TkDefaultFont", size))
    return label

def create_button(frame, text, side="top", fill="both", expand=True, bg=C3):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand, bg)
    # Main
    button = Label(background, text=text, state=state, cursor="hand2")
    button.pack(side=side, fill="both", expand=True)
    button.config(bg=bg, fg="white")
    button.config(height=2, font=("TkDefaultFont", size))
    button.bind("<Button-1>", lambda event: jump_point(text))
    # Hover effect
    button.bind("<Enter>", lambda event: background.config(bg=C4))
    button.bind("<Leave>", lambda event: background.config(bg=bg))
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
    images = image_handler(text, file)
    if expand:
        frame = create_background(background, "right", "both", False, 0, True)
        frame.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
        frame.bind("<Enter>", lambda event: background.config(bg=C4))
        frame.bind("<Leave>", lambda event: background.config(bg=C3))
    else:
        frame = background
    # Main
    label = Label(frame, image=images[text], cursor="hand2")
    label.pack(side="right", expand=False)
    label.config(bg=C3)
    # Binds
    label.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
    label.bind("<Enter>", lambda event: background.config(bg=C4))
    label.bind("<Leave>", lambda event: background.config(bg=C3))
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

def create_row(bg="#323233", borderwidth=0):
    frame = Frame(mainframe, borderwidth=borderwidth)
    frame.pack(side="top", fill="both", expand=True)
    frame.config(bg=bg)
    return frame

def create_square(row, i, side="left"):
    frame1 = Frame(row, borderwidth=5)
    frame1.pack(side=side, fill="both", expand=True)
    frame1.config(bg="#252526")
    frame2 = Frame(frame1)
    frame2.pack(side=side, fill="both", expand=True)
    frame2.config(bg="#323233")
    create_label(frame2, i)

def create_blocklist():
    geometry = root.winfo_geometry()
    print(geometry)
    width = round(mainframe.winfo_width()/250)
    height = round(mainframe.winfo_height()/250)
    print(mainframe.winfo_width(), mainframe.winfo_height())
    for row_i in range(height):
        row = create_row()
        for column_i in range(width):
            create_square(row, f"{column_i}/{row_i}")

class Blocklist:
    
    def __init__(self, frame, items):
        self.columns = round(frame.winfo_width()/250)
        self.rows = round(frame.winfo_height()/250)
        self.block_states = {}
        self.create_grid(frame, len(items))

    def create_grid(self, frame, blocks):
        full_rows = math.floor(blocks/self.columns)
        extra_blocks = blocks % self.columns
        print(full_rows, extra_blocks)
        include_plus_button = True
        for column_id in range(self.columns):
            column = self.create_column(frame)
            # Calculate blocks
            plus_button = False
            blocks = full_rows
            if column_id < extra_blocks:
                blocks += 1
            elif include_plus_button:
                plus_button = True
                include_plus_button = False
            # Create blocks
            self.create_blocks(column, column_id, blocks, plus_button)

    def create_column(self, frame):
        column = Frame(frame, borderwidth=0)
        column.pack(side="left", fill="both", expand=True)
        column.config(bg=C2)
        return column

    def create_blocks(self, column, column_id, active_blocks, plus_button):
        for row_id in range(self.rows):
            if not row_id >= active_blocks:
                self.create_block(column, f"{column_id}/{row_id}")
                self.block_states[f"{column_id}/{row_id}"] = True
            elif plus_button:
                self.create_block(column, "+")
                self.block_states["+"] = True
                plus_button = False
            else:
                self.create_empty(column, f"{column_id}/{row_id}")
                self.block_states[f"{column_id}/{row_id}"] = False

    def create_empty(self, column, block_id):
        # Outer
        block_base = Frame(column, borderwidth=5)
        block_base.pack(side="top", fill="both", expand=True)
        block_base.config(bg=C1)
        # Inner
        block = Frame(block_base)
        block.pack(side="top", fill="both", expand=True)
        block.config(bg=C1)
        block.pack_propagate(0)
        create_label(block, block_id, bg=C1, fg="lightgray")

    def create_block(self, column, block_id):
        # Outer
        block_base = Frame(column, borderwidth=5)
        block_base.pack(side="top", fill="both", expand=True)
        block_base.config(bg="#252526")
        # Inner
        block = Frame(block_base)
        block.pack(side="top", fill="both", expand=True)
        block.config(bg=C3)
        block.pack_propagate(0)
        create_button(block, block_id, "bottom", "both", False)

    def add_button(self, frame):
        create_label(frame, "test")

    def add_block(self, frame):
        pass

    def toggle_colour(self, x, y):
        column = mainframe.slaves()[x]
        block = column.slaves()[y]
        block.config(bg="darkred")

    def refresh(self):
        for item in self.frame.slaves():
            item.destroy()
        Blocklist(self.frame, load_maps())

def multiple(obj_type, amount, frame=True):
    if frame:
        frame = mainframe
    items = []
    for i in range(amount):
        items.append(obj_type(frame))
    return items

def load_maps():
    for path, folders, files in os.walk("maps"):
        pass
    return files

"""

START

"""

def startup():
    switch_frame("Mainmenu")

def jump_point(text):
    text = text.replace("/", " id ")
    match text.split():
    #match re.split(" |/", text):
        case ["Quit"]:
            quit()
        case ["Back"]:
            switch_frame("Mainmenu")
        case [x, "id", y]:
            print(f"{x}/{y}")
            x, y = int(x), int(y)
            test_list.toggle_colour(x, y)
        case ["test"]:
            test_list.refresh()
        case _:
            print(text)
            switch_frame(text)

def switch_frame(frame):
    clear_frame(mainframe)
    if frame == "Mainmenu":
        #create_blocklist()
        global test_list
        test_list = Blocklist(mainframe, load_maps())
        #create_row(mainframe)
        #switch_sidebar(frame)
        create_button(sidebar, "test")
    elif frame == "Play":
        create_label(mainframe, ("test"))
        
    elif frame == "LVL-Selector":
        pass

def switch_sidebar(frame):
    clear_frame(sidebar)

def clear_frame(*frames):
    for frame in frames:
        for item in frame.slaves():
            item.destroy()

root.bind("<Escape>", quit) #sys.exit
root.iconbitmap("icons/blume.ico")
root.title("Pac-man LVL-Editor")
#root.geometry("1000x600+100+100")
#root.minsize(250, 200)
root.attributes('-fullscreen', True)
root.after(6, startup)
root.mainloop()
