from imports import *

class TileListFrame(tk.Frame):

    def __init__(self, top, **kwargs):
        tk.Frame.__init__(self, top, **kwargs)
        ## Layout Stuff
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, width=1, height=1)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.vbar = DynamicScrollbar(self,
                                     orient=tk.VERTICAL,
                                     command=self.canvas.yview
                                     )
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.vbar.set)

        ## Data Stuff
        self.top = top
        #self.trees = {}
        self.tiles = {}
        self.images = {}
        self.active_tile = None

    def _select_single(self,event):
        """select single tile"""
        tiles = self.top.tabs[0].brush.tiles
        for tile in tiles:
            tile.config(bg = "#DDDDDD")
        del tiles[:]
        event.widget.config(bg="green")
        tiles.append(event.widget)


    def _select_mult(self, event):
        """select multiple tiles"""
        tiles = self.top.tabs[0].brush.tiles
        if event.widget in tiles:
            tiles.pop(tiles.index(event.widget))
            event.widget.config(bg = "#DDDDDD")
        else:
            event.widget.config(bg = "green")
            tiles.append(event.widget)


    def _update(self):
        del self.master.tabs[0].brush.tiles[:] # clearing selected tiles list
        y = 0
        trees = {key : self.master.trees[key] for key in self.master.trees if self.master.trees[key].getroot().tag == "tileset"}
        for tree in sorted(trees):
            tileset = trees[tree].getroot()
            image_path = tileset.get("source")
            tiles = tileset.findall("tile")
            for t in tiles:
                dims = int(t.get("x")), int(t.get("y")), int(t.get("x_")), int(t.get("y_"))
                height = int(t.get("height"))
                tid = t.get("id")
                open_image = Image.open(image_path)
                cropped_image = open_image.crop(dims)
                image = ImageTk.PhotoImage(cropped_image)
                self.images[t.get("id")] = image
                tile = Tile(self, tid=tid, image=image)
                self.canvas.create_window(0,y, window=tile, anchor=tk.NW)
                tile.bind("<Button-1>", self._select_single)
                self.tiles[tid] = tile
                for i in self.tiles.keys():
                    print(self.tiles[i].tid)
                y += height
                self.canvas.config(scrollregion=(0,0,0,y))


class Tile(tk.Label):
    """subclass of Label. Containing Tile_ID"""

    def __init__(self, *args, tid=None, **kwargs):
        tk.Label.__init__(self, *args, **kwargs)
        self.tid = tid






