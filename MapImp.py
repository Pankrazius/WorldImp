from imports import *

class MapFrame(tk.Frame):

    def __init__(self,top, **kwargs):
        tk.Frame.__init__(self,top,**kwargs)
        ## Data Stuff
        self.top = top
        self.label = Labels.MAIN_LABEL_MAPEDITOR
        self.tree = MapTree()
        ## Widget Layout Stuff
        self.maps_nb = ParentedNotebook(self)
        self.tools_frame = ToolFrame(self)
        self.maps_nb.grid(row=0, column=0, sticky="nesw")
        self.tools_frame.grid(row=0, column=1, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=90)
        self.grid_columnconfigure(1, weight=10)
        self._createPage()

    def _createPage(self):
        map = MapTab(self.maps_nb)
        self.maps_nb.add(map, text=Labels.MAP_NB_NEW)



class ToolFrame(tk.Frame):

    def __init__(self,top):
        tk.Frame.__init__(self,top)
        ## Data Stuff
        self.top = top


        ## Widget Layout Stuff

class MapTab(tk.Frame):
    """
    An unlimited Map of floor tiles.

    contains Chunks for storing other Screen-Objects
    """

    def __init__(self,top):
        tk.Frame.__init__(self,top)
        ## Data Stuff
        self.top = top
        self.main = top.top.top
        self.chunk_size = 16 # as my chunk is square i just need one value
        self.map_size = [3,3,1] # Size of map in 'chunks'
        self.cell_width = 32
        self.cell_height = 32
        self.orientation = "isometric" # Dummy, put in 'NewProject'-Function
        if self.orientation == "isometric":
            self.cell_size = (self.cell_width*2, self.cell_height)
        else:
            self.cell_size = (self.cell_width, self.cell_height)
        self.map_array = self._createMap()[0]
        self.chunk_array = self._createMap()[1]
        self.chunks = self._createMap()[2]
        # Widget Layout Stuff
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, width=1, height=1, border=1, relief=tk.SUNKEN, bg="cyan")
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.canvas_objects = []
        self.vbar = DynamicScrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar = DynamicScrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        ## Function Stuff
        self.drawGrid()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    def _createMap(self):
        """sets a new empty map"""
        width = self.map_size[0] * self.chunk_size
        height = self.map_size[1] * self.chunk_size
        map_array = np.zeros((height, width), dtype=float)
        chunks = {}
        clist = []
        for i in range(0, self.map_size[0]*self.map_size[1]):
            chunks[i+1] = Chunk()
        chunk_array = np.asarray(list(chunks.keys()))
        chunk_array.resize(self.map_size[0], self.map_size[1])
        return map_array, chunk_array, chunks


    def addChunk(self, direction):
        """adds colums or rows depending on chunk-size"""
        pass

        ## get size of actual map
        ## create array of fitting size
        ## stack created array to map


    def addLevel(self):
        """adds a hight-level to the map."""
        pass

    def drawGrid(self):
        """draw map on canvas, according to it's orientation"""

        if self.orientation == "isometric":
            for vline in range(0, self.map_array.shape[0]):
                line = self.canvas.create_line(iso(vline*self.cell_width, 0),
                                               iso(vline*self.cell_width, self.map_array.shape[0]*self.cell_height))
                self.canvas_objects.append(line)

            for hline in (range(0, self.map_array.shape[1])):
                line = self.canvas.create_line(iso(0, hline*self.cell_height),
                                               iso(self.map_array.shape[1]*self.cell_width, hline*self.cell_height))
                self.canvas_objects.append(line)
        self.canvas.bind("<Button-1>", self.setTile)

    def setTile(self, event):
        e = event.widget
        print("called setTile in MapTab")
        print("EventX = ",event.x, "EventY = ", event.y)
        print("Screenpos = ", int(e.canvasx(event.x)), int(e.canvasy(event.y)))
        cx, cy = cart(e.canvasx(event.x), e.canvasy(event.y))
        print("Carthesian", cx, cy)

        cellx = int(cx) // self.cell_width
        celly = int(cy) // self.cell_height

        print("Cell Coordinates", cellx, celly)
        active_tile = self.main.main_tilelist.active_tile
        if active_tile:
            self.map_array[cellx, celly] = active_tile.tid
        else:
            print("Nothing selected")
            return
        np.set_printoptions(threshold=np.inf)
        print(self.map_array)








class Chunk:
    """
    A multiple Cells sized Map-Chunk

    contains all Screen-Objects above Wall-level
    """

    def __init__(self):
        self.inventory = Inventory(self)


class Cell:
    """
    Basic Cell for Map.
    """
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.tile = None

## Note: Cell could be replaced with simple dictionary.?


class Inventory():
    """
    Basic inventory. Contains dict and link to parent.
    """

    def __init__(self, top):
        self.top = top
        self.items = {}

def iso(x,y):
    isox = x-y
    isoy = (x+y)/2

    return isox, isoy

def cart(x,y):
    cartx = (2*y + x)/2
    carty = (2*y - x)/2

    return cartx, carty


if __name__ == "__main__":

    master = tk.Tk()
    master.minsize(300,300)

    testmap = MapTab(master)
    testmap.pack(expand=1, fill=tk.BOTH)

    master.mainloop()
