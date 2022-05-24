from tkinter import *
from colours import *
import json, math, os
from PIL import ImageTk, Image

root = Tk()

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

def create_button(frame, text, side="top", fill="both", expand=True, bg=C3, fg="white"):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand)
    # Main
    button = Label(background, text=text, state=state, cursor="hand2")
    button.pack(side=side, fill="both", expand=True)
    button.config(bg=bg, fg=fg)
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
    image = Image.open(file).convert("RGBA").rotate(rotation)
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)
    global images
    images[text] = image
    return images[text]

def get_image(file_name, size=90):
    # IV8512
    global loaded_images
    if file_name in loaded_images:
        return loaded_images[file_name]
    else:
        image = image_handler(file_name, f"textures/{file_name}", 90)
        loaded_images[file_name] = image
        return image

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
        self.debug = debug
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
        if self.check_map(ordinal_num + 1):
            create_button(block, (f"Level {ordinal_num+1}", 15), fg=C8)
        else:
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

    def check_map(self, level_id):
        with open(f"data/saved_data.json") as data:
            data = json.load(data)
        try:
            score = data[f"Level {level_id}"]
            return True
        except KeyError:
            return False

    def refresh(self):
        for item in self.frame.slaves():
            item.destroy()
        Blocklist(self.frame, load_maps())

def play_btn():
    with open(f"data/saved_data.json") as data:
        data = json.load(data)
    for i in range(1, len(load_maps())):
        try:
            data[f"Level {i}"]
        except KeyError:
            load_map(i)
            return

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
    frame2.pack_propagate(0)
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
    global current_level, loaded_images
    current_level, loaded_images = 0, {}
    
def jump_point(text, toggle=False):
    match text.split():
        case ["Quit"]:
            quit()
        case ["Back"]:
            switch_frame("Mainmenu")
        case ["Play"]:
            play_btn()
        case ["Reset", "level"]:
            switch_level(current_level, 0)
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
        case ["Reset", "save", "data"]:
            save_data("reset")
            switch_frame("Levels")
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

def switch_sidebar(frame):
    clear_frame(sidebar)
    if frame == "Mainmenu":
        create_label(sidebar, ("Petri-man", 50), "top", "x", True, C3)
        
        menu_bar = create_row(sidebar, fill="x", expand=False, bg=C3)
        create_button(menu_bar, ("Play", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Levels", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Open editor", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Reset save data", 20), "top", "x", True, C3)

        create_label(sidebar, "", "top", "x", True, C2)

        Quit_border = create_row(sidebar, "bottom", "x", False, 5, C3)
        create_button(Quit_border, ("Quit", 20), "bottom", expand=False, bg=C3)

    else:
        create_label(sidebar, ("", 50), "top", "x", False, C2)
        create_label(sidebar, ("level ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("???: ?", 25), "top", "x", False, C3)
        create_label(sidebar, ("", 50), "top", "x", False, C2)
        
        menu_bar = create_row(sidebar, fill="x", expand=False, bg=C3)
        create_button(menu_bar, ("Levels", 20), "top", "x", True, C3)
        create_button(menu_bar, ("Reset level", 20), "top", "x", True, C3)

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
    root.bind("r", lambda event: jump_point("Reset level"))

def position_handler(move=""):
    if movement_validator(move):
        return
    global current_pos
    change_colour(current_pos[0], current_pos[1], "None")

    enemy_move(current_pos)
    if move == "w":
        current_pos[1] -= 1
    elif move == "a":
        current_pos[0] -= 1
    elif move == "s":
        current_pos[1] += 1
    elif move == "d":
        current_pos[0] += 1

    # paint the new current_pos with player color
    change_colour(current_pos[0], current_pos[1], "Player")

    sidebar_updater()

    if current_pos in holes:
        switch_level(current_level, 0)
    elif apples == [] and current_pos in next_level:
        switch_level(current_level, 1)
    elif apples == [] and next_level == []:
        switch_level(current_level, 1)

def movement_validator(key):
    # JL6079
    if key == "w":
        # calculates position if move is made
        new_pos = [current_pos[0], current_pos[1] - 1]
        # checks if new position is invalid
        if new_pos in walls or current_pos[1] - 1 < 0:
            # returns True if you've hit a wall or the edge
            return True
        elif new_pos in next_level and apples != []:
            return True

    elif key == "a":
        new_pos = [current_pos[0] - 1, current_pos[1]]
        if new_pos in walls or new_pos[0] < 0:
            return True
        elif new_pos in next_level and apples != []:
            return True

    elif key == "s":
        new_pos = [current_pos[0], current_pos[1] + 1]
        if new_pos in walls or current_pos[1] + 1 > 10:
            return True
        elif new_pos in next_level and apples != []:
            return True

    elif key == "d":
        new_pos = [current_pos[0] + 1, current_pos[1]]
        if new_pos in walls or current_pos[0] + 1 > 14:
            return True
        elif new_pos in next_level and apples != []:
            return True

    if new_pos in apples:
        score_system("eat_apple", new_pos)
    elif new_pos in bananas:
        score_system("eat_banana", new_pos)
    elif new_pos in coins:
        score_system("eat_coin", new_pos)
    elif new_pos in enemies:
        switch_level(current_level, 0)
    else:
        score_system("move", new_pos)

def sidebar_updater():
    # JL6079
    position_label = sidebar.pack_slaves()[1]
    position_label.config(text=f"Level {current_level}")
    position_label = sidebar.pack_slaves()[2]
    position_label.config(text=f"Score: {score}")
    position_label = sidebar.pack_slaves()[3]
    position_label.config(text=f"Combo: {combo}")
    position_label = sidebar.pack_slaves()[4]
    position_label.config(text=f"Apples left: {len(apples)}")
    position_label = sidebar.pack_slaves()[5]
    position_label.config(text=f"Column: {current_pos[0]}  Row: {current_pos[1]}")

def enemy_move(player_pos):
    global enemies
    # compare if enemy is further away in columns or rows
    for enemy_pos in enemies.copy():
        dist_columns = (enemy_pos[0] - current_pos[0])
        dist_rows = (enemy_pos[1] - current_pos[1])
        if abs(dist_columns) > abs(dist_rows):
            if dist_columns > 0:
                block_update(enemy_pos[0]-1, enemy_pos[1], "Enemy")
            else:
                block_update(enemy_pos[0]+1, enemy_pos[1], "Enemy")
        else:
            if dist_rows < 0:
                block_update(enemy_pos[0], enemy_pos[1]+1, "Enemy")
            else:
                block_update(enemy_pos[0], enemy_pos[1]-1, "Enemy")                
        item = mainframe.slaves()[enemy_pos[0]].slaves()[enemy_pos[1]]
        if enemy_pos in holes:
            change_colour(enemy_pos[0], enemy_pos[1], "Hole")
            clear_frame(item.slaves()[0])
        elif enemy_pos in walls:
            change_colour(enemy_pos[0], enemy_pos[1], "Wall")
            clear_frame(item.slaves()[0])
        elif enemy_pos in apples:
            change_colour(enemy_pos[0], enemy_pos[1], "Apple")
        elif enemy_pos in bananas:
            change_colour(enemy_pos[0], enemy_pos[1], "Banana")
        elif enemy_pos in coins:
            change_colour(enemy_pos[0], enemy_pos[1], "Coin")
        elif enemy_pos in next_level:
            change_colour(enemy_pos[0], enemy_pos[1], "Next level")
        else:
            change_colour(enemy_pos[0], enemy_pos[1], "None")
        enemies.remove([enemy_pos[0], enemy_pos[1]])

# TODO move this
def block_update(column, row, block_type):
    global hole, walls, apples, bananas, coins, next_level
    if block_type == "Player":
        movement_controls(column, row)
    elif block_type == "Hole":
        holes.append([column, row])
    elif block_type == "Wall":
        walls.append([column, row])
    elif block_type == "Enemy":
        enemies.append([column, row])
    elif block_type == "Apple":
        apples.append([column, row])
    elif block_type == "Banana":
        bananas.append([column, row])
    elif block_type == "Coin":
        coins.append([column, row])
    elif block_type == "Next level":
        next_level.append([column, row])
    change_colour(column, row, block_type)

# TODO move this
def load_map(level_id):
    global holes, walls, enemies, apples, bananas, coins, next_level, combo, score, current_level
    holes, walls, enemies, apples, bananas, coins, next_level, combo, score, current_level = [], [], [], [], [], [], [], 0, 0, level_id

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
    # JL6079
    if mod > 0:
        save_data("score")
    global current_level, current_pos
    # add modifier to current level and load corresponding map
    current_level = int(level_id) + mod
    current_pos = [] 
    load_map(current_level)

def save_data(action):
    match action:
        case "score":
            with open("data/saved_data.json", "r") as file:
                data = json.load(file)
            # fetches old top score for the current level from saved_data.json
            try:
                old_score = data[f"Level {current_level}"]["score"]
            except:
                old_score = 0
            # replace old score if new score is higher than the old one
            if old_score <= score:
                data[f"Level {current_level}"] = {"score": max(score, 1)}
            with open("data/saved_data.json", "w") as file:
                json.dump(data, file, indent = 4)
        case "reset":
            data = {}
            with open("data/saved_data.json", "w") as file:
                json.dump(data, file, indent = 4)

def score_system(action, position):
    # JL6079
    global apples, bananas, coins, score, combo
    if action == "eat_apple":
        combo = combo + 3
        score = math.floor(score + (5 * combo))
        apples.remove(position)
    if action == "eat_banana":
        combo = combo + 5
        score = math.floor(score + (1 * combo))
        bananas.remove(position)
    if action == "eat_coin":
        score = math.floor(score + max((100 * combo), 50))
        coins.remove(position)
    elif action == "move":
        combo = max(combo - 1, 0)

def change_colour(column, row, state):
    item = mainframe.slaves()[column].slaves()[row]
    if state == "None":
        item.config(bg=C2)
        item.slaves()[0].config(bg=C3)
        clear_frame(item.slaves()[0])
    elif state == "Hole":
        item.config(bg=C1)
        item.slaves()[0].config(bg=C1)
    elif state == "Wall":
        item.config(bg=C6)
        item.slaves()[0].config(bg=C3)
    elif state == "Player":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "ghost.png")
    elif state == "Enemy":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "pahis.png")
    elif state == "Apple":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "apple.png")
    elif state == "Banana":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "banana.png")
    elif state == "Coin":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "kolikke.png")
    elif state == "Next level":
        clear_frame(item.slaves()[0])
        image_block(item, column, row, "door.png")
    else:
        item.config(bg=C2)
        item.slaves()[0].config(bg=C3)

def image_block(item, column, row, texture, size=100, rotation=0):
    label = Label(item.slaves()[0], image = get_image(texture))
    label.pack()
    label.config(bg=C3)

root.bind("<Escape>", quit) #sys.exit
#root.iconbitmap("blume.ico")
root.title("Petri-man")
#root.geometry("1000x600+100+100")
#root.minsize(250, 200)
root.attributes('-fullscreen', True)
root.after(6, startup)
root.mainloop()
