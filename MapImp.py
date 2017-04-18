from imports import *

class MapFrame(tk.Frame):

    def __init__(self,top):
        tk.Frame.__init__(self,top)
        ## Data Stuff
        self.top = top
        self.label = Labels.MAIN_LABEL_MAPEDITOR
        ## Widget Layout Stuff
        self.maps_nb = ParentedNotebook(self)
        self.tools_frame = ToolFrame(self)
        self.maps_nb.grid(row=0, column=0, sticky="nesw")
        self.tools_frame.grid(row=0, column=1, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=90)
        self.grid_columnconfigure(1, weight=10)



class ToolFrame(tk.Frame):

    def __init__(self,top):
        tk.Frame.__init__(self,top)
        ## Data Stuff
        self.top = top
        self.tree = MapTree()

        ## Widget Layout Stuff

class MapTab(tk.Frame):

    def __init(self,top):
        tk.Frame.__init__(self,top)
        ## Data Stuff
        self.top = top

        # Widget Layout Stuff
        self.canvas = tk.Canvas(self)
