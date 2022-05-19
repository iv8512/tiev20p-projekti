from tkinter import *
from colours import *
import json, math, os
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
        print("cols :", self.columns, "rows: ", self.rows)

    def create_grid(self, frame, blocks):
        full_rows = math.floor(blocks/self.columns)
        extra_blocks = blocks % self.columns
        if self.debug:
            print(full_rows, extra_blocks)
        include_plus_button = False
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
    print("maps loaded: ", len(maps))
    return maps

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
    # makes apples invisible
    # create_label(frame2, i)

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
    global current_level
    current_level = 0

def jump_point(text, toggle=False):
    match text.split():
        case ["Quit"]:
            quit()
        case ["Back"]:
            switch_frame("Mainmenu")
        case ["Level", level_id]:
            load_map(level_id)
        case ["Toggle", *text]:
            text = " ".join(text)
            state = toggle_handler(text)
            if state:
                image = image_handler(text, "Toggle On.png")
            else:
                image = image_handler(text, "Toggle Off.png")
            toggle.configure(image=image)
        case ["Open", "editor"]:
            os.startfile("map_editor.pyw")
            quit()
        case _:
            print("clicked: ", text)
            switch_frame(text)

def switch_frame(frame):
    clear_frame(mainframe)
    if frame == "Mainmenu":
        switch_sidebar(frame)
        
    elif frame == "Play":
        switch_sidebar(frame)
        create_mapgrid(mainframe)
        
    elif frame == "Levels":
        
        mapframe = Frame(mainframe, borderwidth=0)
        mapframe.pack(side="left", fill="both", expand=True)
        maplist = Blocklist(mapframe, load_maps())
        
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
        create_button(menu_bar, ("Levels", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Settings", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Open editor", 20), "top", "x", True, C3)

        create_label(sidebar, "", "top", "x", True, C2)

        Quit_border = create_row(sidebar, "bottom", "x", False, 5, C3)
        create_button(Quit_border, ("Quit", 20), "bottom", expand=False, bg=C3)

    else:
        create_label(sidebar, ("", 50), "top", "x", False, C2)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("", 50), "top", "x", False, C2)
        
        menu_bar = create_row(sidebar, fill="x", expand=False, bg=C3)
        create_button(menu_bar, ("Levels", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Settings", 20), "top", "x", True, C3)

        create_label(sidebar, "", "top", "x", True, C2)

        Quit_border = create_row(sidebar, "bottom", "x", False, 5, C3)
        create_button(Quit_border, ("Back", 20), "bottom", expand=False, bg=C3)

def clear_frame(*frames):
    for frame in frames:
        for item in frame.slaves():
            item.destroy()

def movement_controls(column, row):
    global current_pos
    current_pos = [column, row]
    root.bind("w", lambda event: position_handler("w"))
    root.bind("a", lambda event: position_handler("a"))
    root.bind("s", lambda event: position_handler("s"))
    root.bind("d", lambda event: position_handler("d"))

def position_handler(move=""):
    if movement_validator(move):
        return
    global current_pos
    change_colour(current_pos[0], current_pos[1], "None")
    if move == "w":
        current_pos[1] -= 1
    elif move == "a":
        current_pos[0] -= 1
    elif move == "s":
        current_pos[1] += 1
    elif move == "d":
        current_pos[0] += 1
    change_colour(current_pos[0], current_pos[1], "Player")

    sidebar_updater()
    
    if current_pos in holes:
        switch_level(current_level, 0)

    if apples == []:
        switch_level(current_level, 1)

def sidebar_updater():
    position_label = sidebar.pack_slaves()[1]
    position_label.config(text=f"Score: {score}")
    position_label = sidebar.pack_slaves()[2]
    position_label.config(text=f"Combo: {combo}")
    position_label = sidebar.pack_slaves()[3]
    position_label.config(text=f"Apples left: {len(apples)}")
    position_label = sidebar.pack_slaves()[4]
    position_label.config(text=f"Column: {current_pos[0]} Row: {current_pos[1]}")

# TODO move this
def block_update(column, row, block_type):
    if block_type == "Hole":
        change_colour(column, row, block_type)
        global holes
        holes.append([column, row])
    elif block_type == "Wall":
        change_colour(column, row, block_type)
        global walls
        walls.append([column, row])
    elif block_type == "Player":
        change_colour(column, row, block_type)
        movement_controls(column, row)
    elif block_type == "Apple":
        change_colour(column, row, block_type)
        global apples
        apples.append([column, row])
    else:
        change_colour(column, row, block_type)

# TODO move this
def load_map(level_id):
    global holes, walls, apples, combo, score, current_level
    holes, walls, apples, combo, score, current_level = [], [], [], 0, 0, level_id

    file_name = load_maps()[int(level_id) - 1]
    with open(f"maps/{file_name}") as data:
        data = json.load(data)
    switch_frame("Play")
    print(f"loading {file_name, level_id}")
    for column_index, column_data in enumerate(data["Map"]):
        for row_index, block in enumerate(column_data):
            block_update(column_index, row_index, block)
    sidebar_updater()

def switch_level(level_id, mod):
    global current_level, current_pos
    #add modifier to current level and load corresponding map
    current_level = int(level_id) + mod
    current_pos = []
    
    load_map(current_level)

def movement_validator(key):
    global walls, apples, current_pos
    if key == "w":
        # calculates position if move is made
        new_pos = [current_pos[0], current_pos[1] - 1]
        # checks if new position is invalid
        if new_pos in walls or current_pos[1] - 1 < 0:
            # returns True if you've hit a wall or the edge
            return True
        
    elif key == "a":
        new_pos = [current_pos[0] - 1, current_pos[1]]
        if new_pos in walls or current_pos[0] - 1 < 0:
            return True
        
    elif key == "s":
        new_pos = [current_pos[0], current_pos[1] + 1]
        if new_pos in walls or current_pos[1] + 1 > 10:
            return True
        
    elif key == "d":
        new_pos = [current_pos[0] + 1, current_pos[1]]
        if new_pos in walls or current_pos[0] + 1 > 14:
            return True

    if new_pos in apples:
        score_system("eat", new_pos)
    else:
        score_system("move", new_pos)

def score_system(action, position):
    global apples, score, combo
    
        
    if action == "eat":
        # add to points when apple is eaten
        score = math.floor(score + (50 + 5.5 * combo))
        # delete apple so it can't be eaten again
        apples.remove(position)
        combo = combo + 3
        
    elif action == "move":
        combo = max(combo - 1, 0)

##def score_system(action, position):
##    global apples, score, combo
##    
##    if action == "move":
##        combo = combo + 1
##        
##    elif action == "eat":
##        # add to points when apple is eaten
##        score = score + round(200 / (combo + 1))
##        # delete apple so it can't be eaten again
##        apples.remove(position)
##        combo = 0

def change_colour(column, row, state):
    selected_column = mainframe.slaves()[column]
    # print(len(mainframe.slaves())) = 11
    item = selected_column.slaves()[row]
    if state == "None":
        item.config(bg=C2)
        item.slaves()[0].config(bg=C3)
    elif state == "Hole":
        item.config(bg=C1)
        item.slaves()[0].config(bg=C1)
    elif state == "Wall":
        item.config(bg=C6)
        item.slaves()[0].config(bg=C3)
    elif state == "Player":
        item.config(bg=C8)
        item.slaves()[0].config(bg=C3)
    elif state == "Apple":
        item.config(bg=C2)
        item.slaves()[0].config(bg=C7)
    else:
        item.config(bg=C2)
        item.slaves()[0].config(bg=C3)

root.bind("<Escape>", quit) #sys.exit
#root.iconbitmap("blume.ico")
root.title("Pac-man")
#root.geometry("1000x600+100+100")
#root.minsize(250, 200)
root.attributes('-fullscreen', True)
root.after(6, startup)
root.mainloop()
