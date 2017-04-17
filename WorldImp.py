from imports import *
from MainWindow import MainWindow

def drawMenu(root):
    """MAIN MENU"""
    menu = tk.Menu(root)
    file = tk.Menu(menu, tearoff=0)
    file.add_command(label=Labels.MENU_NEW_PROJECT)
    file.add_command(label=Labels.MENU_LOAD_PROJECT)
    file.add_command(label=Labels.MENU_SAVE_PROJECT)
    file.add_command(label=Labels.MENU_QUIT, command=root.quit)
    menu.add_cascade(label=Labels.MENU_FILE, menu=file)
    edit = tk.Menu(menu, tearoff=0)
    edit.add_command(label=Labels.MENU_SET_GRID)
    edit.add_command(label=Labels.MENU_SHOW_GRID)
    edit.add_command(label=Labels.MENU_HIDE_GRID)
    edit.add_command(label=Labels.MENU_PREFERENCES)
    menu.add_cascade(label=Labels.MENU_EDIT, menu=edit)
    tset = tk.Menu(menu, tearoff=0)
    tset.add_command(label=Labels.MENU_IMPORT, command=main_window.widgets[Labels.MAIN_LABEL_TILESET].loadImage)
    tset.add_command(label=Labels.MENU_EXPORT)
    menu.add_cascade(label=Labels.MENU_TILESET, menu=tset)
    help = tk.Menu(menu, tearoff=0)
    help.add_command(label=Labels.MENU_HELP)
    help.add_command(label=Labels.MENU_VERSION)
    menu.add_cascade(label=Labels.MENU_HELP, menu=help)
    root.config(menu=menu)

if __name__ == "__main__":

    root = tk.Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    main_window = MainWindow(root)
    drawMenu(root)
    root.minsize(int(Dims.WIN_MIN_SIZE[0]), int(Dims.WIN_MIN_SIZE[1]))
    root.mainloop()