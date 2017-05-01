from imports import *

class MapFrame(tk.Frame):

    def __init__(self,top, **kwargs):
        tk.Frame.__init__(self,top,**kwargs)
        ## Data Stuff
        self.top = top
        self.label = Labels.MAIN_LABEL_MAPEDITOR
        self.tree = MapTree()
        self.cell_range = []
        ## Widget Layout Stuff
        self.maps_nb = ParentedNotebook(self)
        self.brush = ToolFrame(self)
        self.maps_nb.grid(row=0, column=0, sticky="nesw")
        self.brush.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, minsize=80)
        self._createPage()

    def _createPage(self):
        map = MapTab(self.maps_nb)
        self.maps_nb.add(map, text=Labels.MAP_NB_NEW)


class ToolFrame(tk.Frame):

    def __init__(self,top,**kwargs):
        tk.Frame.__init__(self,top,**kwargs)
        ## Data Stuff
        self.top = top
        self.tiles = []
        self.eraser = [EraserTile()]

        self.brushes = OrderedDict([("erase", SimpleBrush(self.master, tiles=self.eraser)),
                        ("point", SimpleBrush(self.master, tiles=self.tiles))])
        self.selected = self.brushes["point"]
        self.buttons = []
        ## Widget Layout Stuff
        for b in self.brushes:
            button = tk.Button(self, text=b)
            button.config(command=lambda sel=button, func=b: self.set(sel, func))
            button.pack(fill=tk.X)
            self.buttons.append(button)
        self.config_frame = tk.Frame(self)
        self.config_frame.pack()


    def set(self, selected_button, func):
        for button in self.buttons:
            button.config(bg="grey80", activebackground="grey100")
            selected_button.config(bg="green", activebackground="green")
        print(func)
        self.selected = self.brushes[func]
        print(self.selected)

        #self.selected = self.brushes[func]

        print("Called Function-Change to: ", func)

    #def current(self, event, *args):
    #    self.brushes[self.selected]

    def erase(self, event):
        event.widget.master.setTile(event, tile=0.)

    def point(self, event):
        tid = self.tiles
        if tid:
            event.widget.master.setTile(event, tid[0])

#ToDo: Refactor brush-functions to classes, or get config done otherwise.

class EraserTile:

    def __init__(self):
        self.tid = 0.

class SimpleBrush(object):
    """
    Basic Brush, resizable

    takes: master = master-object, source for area information
           tid = source for tileIds to print

    functions: paint(self, event), paints tile on canvas, sets tileID
                                   in array
               _config(self): internal method, sets config-frame
    """

    def __init__(self, master, tiles):
        self.master = master
        self.size = 1
        self.tiles = tiles
        self._config()

    def paint(self, event):
        if len(self.master.cell_range) > 0 and len(self.tiles) > 0:
            for cell in self.master.cell_range:
                event.widget.master.setTile(cell, tile=self.tiles[0])
            np.set_printoptions(threshold=np.inf)
            print(event.widget.master.map_array)
        else:
            print("Either no size given or no tiles selected")
            return False

    def _config(self):
        pass


class ComplexBrush(SimpleBrush):
    pass


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
        self.tile_dict = {}
        self.chunk_array = self._createMap()[1]
        self.chunks = self._createMap()[2]
        self.celpos = False
        self.brush_frame = False
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
            chunks[i+1] = Chunk(self)
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
        self.canvas.bind("<Button-1>", self.paintCells)
        self.canvas.bind("<Enter>", self.drawFrame)
        self.canvas.bind("<Leave>", self.killFrame)
        self.canvas.bind("<Motion>", self.showFrame)





    def paintCells(self,event):
        cellx, celly = self.getCellpos(event)
        size = self.master.master.brush.selected.size
        del self.master.master.cell_range[:]
        cells = self.getCellRange(cellx, celly, 5)
        self.master.master.cell_range.extend(cells)
        self.master.master.brush.selected.paint(event)
        print(self.master.master.cell_range)
        print(len(self.master.master.cell_range))

    def getCellRange(self, cellx, celly, size):
        """returns list of cells to paint on"""
        y = int(celly - ((size -1) / 2))
        x = int(cellx - ((size -1) / 2))
        _y = int(celly + ((size -1) / 2))
        _x = int(cellx + ((size -1) / 2))
        return list(product(range(x, _x+1), range(y,_y+1)))

    def getCellpos(self, event):
        """returns actual cell the mousepointer is over"""
        e = event.widget
        cx, cy = cart(e.canvasx(event.x), e.canvasy(event.y))
        cellx = int(cx) // self.cell_width
        celly = int(cy) // self.cell_height
        return cellx, celly

    def setTile(self, cell, tile):
        """prints given tile on given cell"""
        assert isinstance(cell, tuple)
        cellx, celly = cell

        if cellx < 0 or cellx > self.map_array.shape[0]-1 or celly < 0 or celly > self.map_array.shape[1]-1:
            return

        if self.tile_dict.get((cellx, celly)):
            self.canvas.delete(self.tile_dict[(cellx, celly)])

        if tile:
            self.map_array[cellx,celly] = tile.tid
            if tile.tid == 0.0:
                return
            map_posx, map_posy = iso(cellx * self.cell_width, celly * self.cell_height)
            image = self.main.main_tilelist.images[tile.tid]
            self.tile_dict[(cellx, celly)] = self.canvas.create_image(map_posx, map_posy, image=image, anchor=tk.N)

    def showFrame(self,event):
        if self.brush_frame:
            cell = self.getCellpos(event)
            if not self.celpos or self.celpos != cell:
                print("Update Celpos; old Celpos is", self.celpos, "new Celpos is", cell)
                oldcell = copy(self.celpos)
                self.celpos = cell
                if oldcell:
                    self.killFrame(event)
                    self.drawFrame(event)



                    #if cell[0] < oldcell[0]:
                    #    print("West")
                    #elif cell[0] > oldcell[0]:
                    #    print("East")
                    #elif cell[1] < oldcell[1]:
                    #    print("North")
                    #elif cell[1] > oldcell[1]:
                    #    print("South")
                else:
                    pass
            else:
                pass

    def drawFrame(self, event):
        print ("entered Canvas, activated draw Frame")
        size = self.master.master.brush.selected.size
        cell = self.getCellpos(event)
        cells = self.getCellRange(cell[0], cell[1], size)
        tl = min(cells)

        nw = iso(tl[0] * self.cell_width, tl[1] * self.cell_height)
        ne = iso((tl[0] + size) * self.cell_width, tl[1] * self.cell_height)
        sw = iso(tl[0] * self.cell_width, (tl[1]+size)* self.cell_height)
        se = iso((tl[0] + size) * self.cell_width, (tl[1] + size) * self.cell_height)
        print(tl)
        print (nw, ne, se, sw)
        self.brush_frame = self.canvas.create_polygon(sw, nw , ne, se, fill = "", outline="red")




        pass

    def killFrame(self, event):
        print("left canvas, activated kill frame function")
        self.canvas.delete(self.brush_frame)
        self.brush_frame = False








#
    def update(self):
        self.canvas.create_image()
        print(self.main.main_tilelist.images)


class Chunk(object):
    """
    A multiple Cells sized Map-Chunk

    contains all Screen-Objects above Wall-level
    """

    def __init__(self, top):
        self.top = top
        self.inventory = Inventory(self)


class Cell(object):
    """
    Basic Cell for Map.
    """
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.tile = None

## Note: Cell could be replaced with simple dictionary.?


class Inventory(object):
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








