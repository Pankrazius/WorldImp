from imports import *

class TileListFrame(tk.Frame):

    def __init__(self, top):
        tk.Frame.__init__(self,top)
        self.top = top
        self.trees = {}
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nesw")


    def _update(self):
        print("called TilesetListFrame._update.")
        y = 0
        open_tk = open("Images/TorweltenStations_n_Ships.png", mode="rb")
        #open_image = Image.open(image_path)
        tkimage = ImageTk.PhotoImage(file=open_tk)
        test = tk.Toplevel(self)
        test.canvas = tk.Canvas(test, border=1)
        test.canvas.grid_columnconfigure(0, weight=1)
        test.canvas.grid_rowconfigure(0, weight=1)
        test.canvas.grid(sticky="nesw")
        test.canvas.create_rectangle((10,10,30,30))
        test.canvas.create_image(0, 0, image=tkimage, anchor=tk.NW)

        for tree in sorted(self.trees):
            image_path = os.getcwd()+"/"+(self.trees[tree].find("tileset").get("image_path"))
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
                print(cropped_image)
                image = ImageTk.PhotoImage(cropped_image)
                print(image)
                self.canvas.create_image(0, y, image=image, anchor=tk.NW)
                #self.canvas.create_rectangle(0, y, dims[2]-dims[0], y+dims[3]-dims[1], outline="blue")
                y += height

        # Do something like "for every tree (in order), give me every single tile - nested for-loop.
        # Will make this after lunch.