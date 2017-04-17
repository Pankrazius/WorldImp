from imports import *
from TileImp import TilesetFrame
from TileListFrame import TileListFrame


class MainWindow(tk.Frame):
    """Contains all sub-modules packed in a notebook"""

    def __init__(self, top):
        tk.Frame.__init__(self, top)
        self.top = top
        self.grid(row=0, column=0, sticky="nesw")
#        self.grid_rowconfigure(0, weight=1)
#        self.grid_columnconfigure(0, weight=10)
#        self.grid_columnconfigure(1, weight=90)
        self.main_tilelist = TileListFrame(self)
        self.main_tilelist.place(relx=0, rely=0, relwidth=0.1, relheight=1.0)
#        self.main_tilelist.grid(row=0, column=0, sticky="nesw")
        self.main_notebook = ParentedNotebook(self)
        self.main_notebook.place(relx=0.1, rely=0, relwidth=0.9, relheight=1.0)
#        self.main_notebook.grid(row=0, column=1, sticky="nesw")
        # insert scrollable list of tiles here. probably as tree.
        self.tabs = [TilesetFrame(self)]
        self.dummy_tree = ProjectTree("dummy project")  # dummy. replace with function later.
        self.tilelist = [] # dummy place in map-window
        self.widgets = {}
        self.trees = {} # Save the trees!
        self._createNotebook()

    def _createNotebook(self):
        for tabclass in self.tabs:
            tab = tabclass
            self.main_notebook.add(tab, text=tab.label)
            self.widgets[tab.label] = tab
