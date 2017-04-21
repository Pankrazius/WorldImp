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
        self.trees = {}
        self.tiles = {}
        self.images = {}
        self.active_tile = None

    def _activate(self, event):
        print("klicked Label")
        event.widget.config(bg="green")
        self.active_tile = event.widget
        print(event.widget.tid)


    def _update(self):
        print("called TilesetListFrame._update.")
        y = 0

        #open_image = Image.open(image_path)

        for tree in sorted(self.trees):
            image_path = os.getcwd() + "/" + (self.trees[tree].find("tileset").get("image_path"))
            #image = self.top.images[image_path]

            tiles = (list(self.trees[tree].find("tileset")))
            #print(image_path)
            #print(tiles)
            for t in tiles:
                dims = int(t.get("x")), int(t.get("y")), int(t.get("x_")), int(t.get("y_"))
                height = int(t.get("height"))
                tid = t.get("tid")
                print(dims)
                open_image = Image.open(image_path)
                print(open_image)
                cropped_image = open_image.crop(dims)
                image = ImageTk.PhotoImage(cropped_image)
                self.images[t.get("tid")] = image
                print(self.tiles)
                tile = Tile(self.canvas, tid, image=image)
                tile.bind("<Button-1>", self._activate)

                tile_return = self.canvas.create_window(0,y, window=tile, anchor=tk.NW)
                self.tiles[tile_return]= tile

                for i in self.tiles.keys():
                    print(self.tiles[i].tid)


                y += height
                self.canvas.config(scrollregion=(0,0,0,y))


class Tile(tk.Label):
    """subclass of Label. Containing Tile_ID"""

    def __init__(self, top, tid, **kwargs):
        tk.Label.__init__(self, top, **kwargs)
        self.top = top
        self.tid = tid
        self.state = False





