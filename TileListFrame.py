from imports import *

class TileListFrame(tk.Frame):

    def __init__(self, top):
        tk.Frame.__init__(self,top)
        self.top = top
        self.trees = {}
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.tiles = {}



    def _update(self):
        print("called TilesetListFrame._update.")
        y = 0

        #open_image = Image.open(image_path)

        for tree in sorted(self.trees):
            image_path = os.getcwd() + "/" + (self.trees[tree].find("tileset").get("image_path"))
            image = self.top.images[image_path]

            tiles = (list(self.trees[tree].find("tileset")))
            print(image_path)
            print(tiles)
            for tile in tiles:
                dims = int(tile.get("x")), int(tile.get("y")), int(tile.get("x_")), int(tile.get("y_"))
                height = int(tile.get("height"))
                print(dims)
                open_image = Image.open(image_path)
                print(open_image)
                cropped_image = open_image.crop(dims)
                image = ImageTk.PhotoImage(cropped_image)
                self.tiles[tile.get("tid")] = image
                print(self.tiles)
                label = tk.Label(self.canvas, image=image)
                label.image = image
                self.canvas.create_window(0, y, window=label, anchor=tk.NW)
                #self.canvas.create_rectangle(0, y, dims[2]-dims[0], y+dims[3]-dims[1], outline="blue")
                y += height

        # Do something like "for every tree (in order), give me every single tile - nested for-loop.
        # Will make this after lunch.