from tkinter import *
from interactables import *

root = Tk()

mainframe = Frame(root)
mainframe.pack(side="top", fill="both", expand=True)
mainframe.config(bg="#1B1B1B")

padding = Frame(mainframe)
padding.pack(side="top", fill="none", expand=True)
padding.config(bg="#323233")
padding.config(width=400, height=150)
padding.pack_propagate(0)

menubar = Frame(mainframe)
menubar.pack(side="top", fill="x", expand=True)
menubar.config(bg="#323233")



create_label(padding, ("Pac-man", 50), fill="none", expand=True)
create_button(menubar, ("Play", 20), "left", "x", True)
create_button(menubar, ("LVL-Selector", 20), "left", "x", True)
create_button(menubar, ("Settings", 20), "left", "x", True)

root.title("Pac-man")
root.geometry("1000x600+100+100")
root.minsize(250, 200)
root.mainloop()
