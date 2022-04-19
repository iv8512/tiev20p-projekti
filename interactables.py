from tkinter import *

import os
try:
    from PIL import ImageTk, Image
except ModuleNotFoundError:
    os.system('cmd /c "pip install Pillow"')
    from PIL import ImageTk, Image

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

def create_label(frame, text, expand=True):
    text, size, state = text_handler(text)
    label = Label(frame, text=text, state=state)
    label.pack(side="top", fill="both", expand=expand)
    label.config(fg="white", bg="#323233")
    label.config(font=("TkDefaultFont", size))

def create_button(frame, text, side="top", fill="both", expand=True):
    # Other
    text, size, state = text_handler(text)
    background = create_background(frame, side, fill, expand)
    # Main
    button = Label(background, text=text, state=state, cursor="hand2")
    button.pack(side=side, fill="both", expand=True)
    button.config(bg="#323233", fg="white")
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

if __name__ == '__main__':

    def jump_point(text, toggle=False):
        print(text.split())
        match text.split():
            case ["Toggle", *text]:
                text = " ".join(text)
                state = toggle_handler(text)
                if state:
                    images = image_handler(text, "Toggle On.png")
                else:
                    images = image_handler(text, "Toggle Off.png")
                toggle.configure(image=images[text])
            case _:
                width = root.pack_slaves()[3].winfo_width()
                height = root.pack_slaves()[3].winfo_height()
                print(width, height)

    root= Tk()

    create_label(root, "label")
    create_button(root, "button 1", expand=False)
    create_button(root, "button 2")
    create_toggle(root, "toggle 1", expand=False)
    create_toggle(root, "toggle 2")

    root.geometry("300x300")
    root.mainloop()
