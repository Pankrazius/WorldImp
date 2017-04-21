from imports import *
from TileImp import TilesetFrame
from TileListFrame import TileListFrame
from MapImp import MapFrame


class MainWindow(tk.Frame):
    """Contains all sub-modules packed in a notebook"""

    def __init__(self, top):
        tk.Frame.__init__(self, top)
        ## Layout Stuff
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=15)
        self.columnconfigure(1, weight=85)
        self.main_tilelist = TileListFrame(self)
        self.main_tilelist.grid(row=0, column=0, sticky="nesw")
        self.main_notebook = ParentedNotebook(self)
        self.main_notebook.grid(row=0, column=1, sticky="nesw")
        ## Data Stuff
        self.check = "You are at MainWindow"
        self.top = top
        self.tabs = [MapFrame(self),TilesetFrame(self)]
        self.dummy_tree = ProjectTree()  # dummy. replace with function later.
        self.widgets = {}
        self.trees = {} # Save the trees!
        ## Function Stuff
        self._createNotebook()

    def _createNotebook(self):
        for tabclass in self.tabs:
            tab = tabclass
            self.main_notebook.add(tab, text=tab.label)
            self.widgets[tab.label] = tab

if __name__ == "__main__":

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.minsize(int(Dims.WIN_MIN_SIZE[0]), int(Dims.WIN_MIN_SIZE[1]))
    app = MainWindow(root)
    root.mainloop()