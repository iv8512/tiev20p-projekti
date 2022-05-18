from tkinter import *
from colours import *
import json, math, os
from PIL import ImageTk, Image
"""pip install pillow"""
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
        self.frame = self.text_handler("frame")
        
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
    background = create_background(frame, side, fill, expand, C3)
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
    if expand:
        frame = create_background(background, "right", "both", False, C3, 0, True)
        frame.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
        frame.bind("<Enter>", lambda event: background.config(bg=C4))
        frame.bind("<Leave>", lambda event: background.config(bg=C3))
    else:
        frame = background
    # Main
    label = Label(frame, image=image_handler(text, file), cursor="hand2")
    label.pack(side="right", expand=False)
    label.config(bg=C3)
    # Binds
    label.bind("<Button-1>", lambda event: jump_point(f"Toggle {text}", label))
    label.bind("<Enter>", lambda event: background.config(bg=C4))
    label.bind("<Leave>", lambda event: background.config(bg=C3))
    return label

def image_handler(text, file, size=40, rotation=0):
    # JL6079
    image = Image.open(file).convert("RGBA").rotate(rotation)
    image = image.resize((size, size), Image.Resampling.LANCZOS)
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

def create_frame(frame, side="top", fill="both", expand=True, border=0, bg=C2):
    frame = Frame(frame, borderwidth=border)
    frame.pack(side=side, fill=fill, expand=expand)
    frame.config(bg=bg)
    return frame

def create_row_old(bg="#323233", borderwidth=0):
    frame = Frame(mainframe, borderwidth=borderwidth)
    frame.pack(side="top", fill="both", expand=True)
    frame.config(bg=bg)
    return frame

def create_square_old(row, i, side="left"):
    frame1 = Frame(row, borderwidth=5)
    frame1.pack(side=side, fill="both", expand=True)
    frame1.config(bg="#252526")
    frame2 = Frame(frame1)
    frame2.pack(side=side, fill="both", expand=True)
    frame2.config(bg="#323233")
    create_label(frame2, i)

def create_blocklist_old():
    geometry = root.winfo_geometry()
    print(geometry)
    width = round(mainframe.winfo_width()/250)
    height = round(mainframe.winfo_height()/250)
    print(mainframe.winfo_width(), mainframe.winfo_height())
    for row_i in range(height):
        row = create_row()
        for column_i in range(width):
            create_square(row, f"{column_i}/{row_i}")

class Create:

    def __init__(self, frame):
        self.frame = frame

    def create_column(self, frame):
        column = Frame(frame, borderwidth=0)
        column.pack(side="left", fill="both", expand=True)
        column.config(bg=C2)
        return column

    def create_block(self, column, bg=C2, fg=C3):
        # Outer
        block_base = Frame(column, borderwidth=5)
        block_base.pack(side="top", fill="both", expand=True)
        block_base.config(bg=bg)
        # Inner
        block = Frame(block_base)
        block.pack(side="top", fill="both", expand=True)
        block.config(bg=fg)
        block.pack_propagate(0)
        return block_base, block

class Blocklist(Create):
    
    def __init__(self, frame, items, debug=False):
        super().__init__(frame)
        self.items = items
        #self.include_plus_button = plus_button
        self.debug = debug
        #self.columns = round(frame.winfo_width()/250)
        #self.rows = round(frame.winfo_height()/250)
        self.columns = 9
        self.rows = 6
        self.block_states = {}
        self.create_grid(frame, len(items))

    def create_grid(self, frame, blocks):
        full_rows = math.floor(blocks/self.columns)
        extra_blocks = blocks % self.columns
        if self.debug:
            print(full_rows, extra_blocks)
        include_plus_button = True
        for column_id in range(self.columns):
            column = super().create_column(frame)
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

    def create_blocks(self, column, column_id, active_blocks, plus_button):
        for row_id in range(self.rows):
            if not row_id >= active_blocks:
                ordinal_num = self.columns * row_id + column_id
                self.create_true(column, f"{column_id}/{row_id}", ordinal_num)
                self.block_states[f"{column_id}/{row_id}"] = True
            elif plus_button:
                self.create_plus_button(column, "+")
                self.block_states["+"] = True
                plus_button = False
            else:
                self.create_false(column, f"{column_id}/{row_id}")
                self.block_states[f"{column_id}/{row_id}"] = False

    def create_true(self, column, block_id, ordinal_num):
        """Create a light block"""
        block = super().create_block(column)[1]
        create_button(block, (f"Level {ordinal_num+1}", 15))
        if self.debug:
            create_label(block, self.items[ordinal_num])
            create_label(block, ordinal_num)
            create_label(block, block_id, "bottom", "both", False)

    def create_false(self, column, block_id):
        """Create a dark block"""
        block = super().create_block(column, C1, C1)[1]
        if self.debug:
            create_label(block, block_id, bg=C1, fg="lightgray")

    def create_plus_button(self, column, block_id):
        block_base, block = super().create_block(column, C1, C1)
        image = image_handler("+", "icons/Disabled.png", 125, 45)
        label = Label(block, image=images["+"], cursor="hand2", bg=C1)
        label.pack(side="top", fill="both", expand=True)
        label.bind("<Button-1>", lambda event: self.plus_function())
        label.bind("<Enter>", lambda event: block_base.config(bg=C4))
        label.bind("<Leave>", lambda event: block_base.config(bg=C1))

    def plus_function(self):
        new_map()
        self.refresh()

    def refresh(self):
        for item in self.frame.slaves():
            item.destroy()
        Blocklist(self.frame, load_maps())

class CreateMap(Create):

    def __init__(self, frame, level_id):
        super().__init__(frame)
        self.level_id = level_id
        self.paint_type = 1
        self.map_data = self.load_data()["Map"]
        self.load_map()

    def load_map(self):
        for column_id, column_data in enumerate(self.map_data):
            column = super().create_column(self.frame)
            for row_id, row_data in enumerate(column_data):
                if row_data == 0:
                    block = super().create_block(column, C2)[1]
                elif row_data == 1:
                    block = super().create_block(column, C6)[1]
                elif row_data == 2:
                    block = super().create_block(column, C8)[1]
                elif row_data == 3:
                    block = super().create_block(column, C7)[1]
                create_button(block, f"{column_id}/{row_id}")

    def load_data(self):
        with open(f"maps/level_{self.level_id}.json") as data:
            data = json.load(data)
        return data

    def change_colour(self, column, row):
        column = mainframe.slaves()[column]
        block = column.slaves()[row]
        if self.paint_type == 0:
            block.config(bg=C2)
        elif self.paint_type == 1:
            block.config(bg=C6)
        elif self.paint_type == 2:
            block.config(bg=C8)
        elif self.paint_type == 3:
            block.config(bg=C7)

def multiple(obj_type, amount, frame=True):
    if frame:
        frame = mainframe
    items = []
    for i in range(amount):
        items.append(obj_type(frame))
    return items

def load_maps():
    maps = []
    for path, folders, files in os.walk("maps"):
        for i, file in enumerate(files):
            if "template" in file:
                continue
            with open(f"maps/{file}") as data:
                data = json.load(data)
            maps.append(file)
    maps.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    return maps

def new_map():
    map_id = len(load_maps()) + 1
    print(f"creating new map file level_{map_id}.json")

    with open("maps/map_template.json") as data:
        data = json.load(data)
    
    with open(f"maps/level_{map_id}.json", "w") as file:
        json.dump(data, file, indent=4)

"""

START

"""

def startup():
    switch_frame("Mainmenu")

def jump_point(text, toggle=False):
    text = text.replace("/", " id ")
    match text.split():
    #match re.split(" |/", text):
        case ["Quit"]:
            quit()
        case ["Refresh"]:
            maplist.refresh()
            switch_sidebar("Mainmenu")
        case ["Back"]:
            switch_frame("Mainmenu")
        case ["Level", level_id]:
            switch_sidebar("Level info", level_id)
        case ["Load", "map"]:
            level_id = sidebar.slaves()[1].cget("text").split()[1]
            switch_frame("Load map", level_id)
        case [column, "id", row]:
            print(f"{column}/{row}")
            column, row = int(column), int(row)
            mapgrid.change_colour(column, row)
            mapgrid.map_data[column][row] = mapgrid.paint_type
        case ["Paint", "type", paint_type]:
            paint_type = int(paint_type)
            mapgrid.paint_type = paint_type
            sidebar.slaves()[3].config(text=f"Selected paint: {paint_type}")
        case ["Save", "changes"]:
            with open(f"maps/level_{mapgrid.level_id}.json", "w") as file:
                json.dump({"Map": mapgrid.map_data}, file, indent=4)
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

def switch_frame(frame, level_id=False):
    clear_frame(mainframe)
    if frame == "Mainmenu":
        global maplist
        maplist = Blocklist(mainframe, load_maps())
        switch_sidebar(frame)
    elif frame == "Load map":
        global mapgrid
        mapgrid = CreateMap(mainframe, level_id)
        switch_sidebar(frame, level_id)

def switch_sidebar(frame, level_id=False):
    clear_frame(sidebar)
    if frame == "Mainmenu":
        create_label(sidebar, ("Level info", 20), expand=False, bg=C2)
        create_label(sidebar, "Click on a map to continue", bg=C2)
        create_button(sidebar, ("Quit", 15), "left")
        create_button(sidebar, ("Refresh", 15), "left")
    elif frame == "Level info":
        create_label(sidebar, ("Level info", 20), expand=False, bg=C2)
        create_label(sidebar, (f"Level {level_id}", 15), expand=False, bg=C2)
        create_label(sidebar, "", bg=C2)
        map_size, high_score = load_map_info(level_id)
        create_label(sidebar, (f"Map size: {map_size}", 13))
        create_label(sidebar, "{high_score}")
        create_label(sidebar, "something")
        create_label(sidebar, "", bg=C2)
        create_button(sidebar, ("Load map", 15), expand=False)
        create_button(sidebar, ("Quit", 15), "left")
        create_button(sidebar, ("Refresh", 15), "left")
    elif frame == "Load map":
        create_label(sidebar, ("Level info", 20), expand=False, bg=C2)
        create_label(sidebar, (f"Level {level_id}", 15), expand=False, bg=C2)
        create_label(sidebar, "", bg=C2)
        create_label(sidebar, ("Selected paint: 1", 15), expand=False)
        create_button(sidebar, "Paint type 0", expand=False)
        create_button(sidebar, "Paint type 1", expand=False)
        create_button(sidebar, "Paint type 2", expand=False)
        create_button(sidebar, "Paint type 3", expand=False)
        create_label(sidebar, "", bg=C2)
        create_button(sidebar, ("Save changes", 15), expand=False)
        create_button(sidebar, ("Back", 15), "left")

def load_map_info(level_id):
    with open(f"maps/level_{level_id}.json") as data:
        data = json.load(data)
    map_size = f"{len(data['Map'])}x{len(data['Map'][0])}"
    return map_size, 0

def clear_frame(*frames):
    for frame in frames:
        for item in frame.slaves():
            item.destroy()

root.bind("<Escape>", quit) #sys.exit
root.iconbitmap("icons/blume.ico")
root.title("Pac-man LVL-Editor")
#root.geometry("1000x600+100+100")
#root.minsize(250, 200)
root.state('zoomed')
#root.attributes('-fullscreen', True)
root.after(6, startup)
root.mainloop()
