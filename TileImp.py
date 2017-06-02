from imports import *


class TilesetFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        ## Layout Stuff
        self.grid(row=0, column=0, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=90)
        self.label = Labels.MAIN_LABEL_TILESET
        self.tile_editor = TileEditorFrame(self)
        self.tile_editor.config(bd=1, relief=tk.SUNKEN)
        self.tile_editor.grid(row=0, column=0, sticky="nesw")
        self.tileset_nb = ParentedNotebook(self)
        self.tileset_nb.grid(row=0, column=1, sticky="nesw")
        ## Function Stuff
        self._createTab()

    def _createTab(self):
        """Private Methode of TilesetFrame, creates new TabFrame in TilesetFrame.nb"""
        page = TabFrame(self.tileset_nb)
        print("Tab Name: ",page._name)
        self.tileset_nb.add(page, text=Labels.TILESET_NB_NEW)

    def _getTab(self):
        """Private Methode of TilesetFrame, returns the actual selected TabFrame-Object"""
        key = self.tileset_nb.select().split(".")[-1]
        return self.tileset_nb.children[key]

    def _checkFile(self, filename):
        """
        Checks if <filename> is already added to project-tree.

        arguments: filename String; a filepath returned from loadImage func.

        returns: False if filename is in project-tree; True otherwise
        """
        print(self.master.check)
        n = filename.split("/")
        name1 = n[-1].split(".")[0]
        tree = self.master.project_tree
        name_list = tree.find("tilesets").findall("tileset")
        print(name_list)
        if len(name_list) > 0:
            for name in name_list:
                if name1 == name.get("file_path").split("/")[-1].split(".")[0]:
                    return False
        else: return True
        return True

    def loadImage(self, load_from_tree=None):
        if load_from_tree == None:
            project = self.master.project_tree.getroot()
            options = {"filetypes": [("PNG image", ".png"), ("JPEG image", ".jpg")], "initialdir": os.getcwd()}
            filename = tkfd.askopenfilename(**options)
        else:
            filename = load_from_tree
        if filename:
            if self._checkFile(filename) == False:
                print("Image of same name already opened.")
                return False

            tab = self._getTab()
            if tab.tkimage is None:
                with open(filename, mode="rb") as file:

                    id_ = self.master.newId("tilesets")
                    name = "tileset_"+str(id_)+".xml"
                    ## Check if ImageFile is inside the Projekt-Tree
                    tab.imagepath = filename

                    self.master.images[id_] = Image.open(tab.imagepath)
                    tab.tkimage = ImageTk.PhotoImage(self.master.images[id_]) #file=file
                    self.tileset_nb.tab(tab, text=name)
                    tab.setTileset(name, tab.imagepath)
                    tab.canvas.create_image(0, 0, image=tab.tkimage, anchor=tk.NW)
                    tab.canvas.config(scrollregion=(0, 0, tab.tkimage.width(), tab.tkimage.height()))
                    tab.canvas.bind("<ButtonPress-1>", tab._onButtonPress)
                    tab.canvas.bind("<B1-Motion>", tab._onMotionPress)
                    tab.canvas.bind("<ButtonRelease-1>", tab._onButtonRelease)
                    self._createTab()

            else:
                print("Tab already in use, use new tab.")
        else:
            print("No file provided")




class TabFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        ## Data Stuff
        self.created = False
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.config(borderwidth=1, relief=tk.SUNKEN)
        self.main = self.master.master.master
        self.imagepath = None
        #self.image = None
        self.tkimage = None
        self.rect = Rectangle(self)
        self.tileset = None
        self.key = None
        self.grid_lines = []
        self.ts_width = Dims.GRID_WIDTH
        self.ts_height = Dims.GRID_HEIGHT
        self.ts_lmargin = Dims.GRID_LMARGIN
        self.ts_tmargin = Dims.GRID_TMARGIN
        self.tss_width = tk.StringVar()
        self.tss_height = tk.StringVar()
        self.tss_lmargin = tk.StringVar()
        self.tss_tmargin = tk.StringVar()
        ## Layout Stuff
        self.canvas = tk.Canvas(self)#, width=1, height=1)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.vbar = DynamicScrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar = DynamicScrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.buttonframe = tk.Frame(self, bd=1, relief=tk.RIDGE)
        self.buttonframe.grid(row=2, column=0, sticky="nesw")
        ## Buttons
        self.apply_button = tk.Button(self.buttonframe,
                                      text=Labels.BUTTON_APPLY,
                                      state=tk.DISABLED,
                                      command=self.makeTile)
        self.apply_button.pack(side=tk.LEFT, anchor=tk.NW)
        self.scrap_button = tk.Button(self.buttonframe,
                                      text=Labels.BUTTON_SCRAP,
                                      state=tk.DISABLED,
                                      command=self.scrapSelection)
        self.scrap_button.pack(side=tk.LEFT, anchor=tk.NW)
        self.set_grid_button = tk.Button(self.buttonframe,
                                         text=Labels.BUTTON_SET_GRID,
                                         state=tk.DISABLED)
        self.set_grid_button.pack(side=tk.LEFT, anchor=tk.NW)
        self.show_grid_button = tk.Button(self.buttonframe,
                                          text=Labels.BUTTON_SHOW_GRID,
                                          command=self.showGrid, state=tk.DISABLED)
        self.show_grid_button.pack(side=tk.LEFT, anchor=tk.NW)
        self.toggle_freeform = tk.IntVar()
        self.toggle_freeform_checkbutton = tk.Checkbutton(self.buttonframe,
                                                          text=Labels.BUTTON_TOGGLE_FREEFORM,
                                                          variable=self.toggle_freeform,
                                                          state=tk.DISABLED,
                                                          command=self.toggleFreeform
                                                          )
        self.toggle_freeform_checkbutton.pack(side=tk.LEFT, anchor=tk.NW)

    def _onButtonPress(self, event):  # get origin of rect
        e = event.widget
        if self.rect.set is False:
            print(event.x, event.y)
            self.rect.x1 = e.canvasx(event.x)
            self.rect.y1 = e.canvasy(event.y)
            cell_x1, cell_y1 = self._getCell(self.rect.x1, self.rect.y1)
            print("Rectangle set on", cell_x1, cell_y1)
            self.rect.rect = self.canvas.create_rectangle(cell_x1, cell_y1, cell_x1+self.ts_width,
                                                          cell_y1+self.ts_height, outline="red")
        else:
            print("Selection already set. Scrap or apply selection")

    def _onMotionPress(self, event):  # determine size of rect
        e = event.widget
        if self.rect.set is False:

            self.rect.x2 = e.canvasx(event.x)
            self.rect.y2 = e.canvasy(event.y)
            print("My moving X", self.rect.x2)
            print("My moving Y", self.rect.y2)
            cell_x1, cell_y1 = self._getCell(self.rect.x1, self.rect.y1)
            cell_x2, cell_y2 = self._getCell(self.rect.x2, self.rect.y2)
            print("Rectangle moves to", cell_x2, cell_y2)
            w, h = e.winfo_width(), e.winfo_height()
            # scroll canvas if we reach the borders
            if event.x > 0.9*w:
                e.xview_scroll(1, 'units')
            elif event.x < 0.1*w:
                e.xview_scroll(-1, 'units')
            if event.y > 0.9*h:
                e.yview_scroll(1, 'units')
            elif event.y < 0.1*h:
                e.yview_scroll(-1, 'units')
            # determine wich coord is top/left

            if self.rect.x1 <= self.rect.x2:
                x, x_ = cell_x1*self.ts_width, cell_x2*self.ts_width
            else:
                x, x_ = cell_x2*self.ts_width, cell_x1*self.ts_width+self.ts_width
            if self.rect.y1 <= self.rect.y2:
                y, y_ = cell_y1*self.ts_height, cell_y2*self.ts_height
            else:
                y, y_ = cell_y2*self.ts_height, cell_y1*self.ts_height+self.ts_height
            self.canvas.coords(self.rect.rect, x, y, x_, y_)
            print("cell_x1", cell_x1, "cell_y1", cell_y1, "cell_x2", cell_x2, "cell_y2",cell_y2)
            print("rect.x1, rect.x2, rect.y1, rect.y2", self.rect.x1, self.rect.y1, self.rect.x2, self.rect.y2)
            print("X, X_, Y, Y_", x, y, x_, y_)


    def _onButtonRelease(self, event):  # resetting mouse, scrap rect on new click
        if self.rect.set is False:
            self.apply_button.config(state=tk.NORMAL)
            self.rect.setup()

    def _getCell(self, x, y):
        return (x - self.ts_lmargin )// self.ts_width, (y - self.ts_tmargin) // self.ts_height

    def makeTile(self):
        images = self.master.master.master.images
        id_ = self.tileset.get("id")
        print("MyImage is: ",images[id_])
        print(self.rect.gx1, self.rect.gy1, self.rect.gx2, self.rect.gy2)
        cropped = images[id_].crop((self.rect.gx1, self.rect.gy1, self.rect.gx2, self.rect.gy2))
        self.tile_image = ImageTk.PhotoImage(cropped)
        tile = newTile(self)
        print ("tile in makeTile", tile)
        tile_editor = self.master.master.tile_editor
        tile_editor.tile_element = tile
        tile_editor.current_tileset = self.tileset
        tile_editor.current_tab = self
        print("Self Element in MakeTile ", self.tileset)
        tile_editor.drawImages(self.tile_image)
        tile_editor.confirm_button.config(state=tk.NORMAL)

    def scrapSelection(self):  # scrap actual selection, resetting temporary variables
        print("called scrapSelection", self)
        self.canvas.delete(self.rect.rect)
        self.rect._reset()
        print(self.rect.set)

    def showGrid(self):
        if self.ts_height > 1 and self.ts_width > 1:
            if not self.grid_lines:
                for vline in range(self.ts_lmargin, self.tkimage.width(), self.ts_width):
                    line = self.canvas.create_line(vline, 0, vline, self.tkimage.height())
                    self.grid_lines.append(line)
                for hline in range(self.ts_tmargin, self.tkimage.height(), self.ts_height):
                    line = self.canvas.create_line(0, hline, self.tkimage.width(), hline)
                    self.grid_lines.append(line)
                self.show_grid_button.config(text=Labels.BUTTON_HIDE_GRID)
            else:
                for line in self.grid_lines:
                    self.canvas.delete(line)
                self.grid_lines.clear()
                self.show_grid_button.config(text=Labels.BUTTON_SHOW_GRID)
        else: return

    def toggleFreeform(self):
        pass

    def setTileset(self, name, source):
        id_ = self.main.newId("tilesets")
        # update ProjectTree
        project = self.main.project_tree.getroot()
        tilesets = project.find("tilesets")
        tilesets_path = tilesets.get("path")
        update = updateProjectTree("tileset", name, id_)
        tilesets.append(update)
        # build TilesetTree

        self.tileset = newTileset(name, id_, source, tilesets_path)
        tileset_tree = ElementTree(self.tileset)
        self.key = "tileset_"+self.tileset.get("id")
        self.main.trees[self.key] = tileset_tree
        print("TreeList ",self.main.trees)
        print("Dumping TilesetElement")
        et.dump(self.tileset)
        print("Dumping Project")
        et.dump(project)
        # Update TabFrame
        self.created = True
        # Update TileList
#        self.main.main_tilelist.trees[id_] = self.tileset
        ## Activate Buttons
        self.apply_button.config(state=tk.NORMAL)
        self.scrap_button.config(state=tk.NORMAL)

class TileEditorFrame(tk.Frame):
    """For editing single Tiles"""
    def __init__(self, *args, **kwargs):
        ## Data Stuff
        tk.Frame.__init__(self, *args, **kwargs)
        self.main = self.master.master
        self.created = False
        self.tile_image = None
        self.tile_element = None
        self.tile = {}
        self.current_tab = None
        self.current_tileset = None
        self.current_ts_id = None
        self.has_animation = tk.StringVar()
        self.has_seasons = tk.StringVar()
        self.has_idle = tk.StringVar()
        self.is_activator = tk.StringVar()
        self.is_container = tk.StringVar()
        self.is_door = tk.StringVar()
        self.has_lock = tk.StringVar()
        ## Layout Stuff
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=7)
        self.config(border=1, relief=tk.SUNKEN)
        self.tile_canvas = tk.Canvas(self, width=1, height=1)
        self.tile_canvas.grid(row=0, column=0, sticky="nesw")
        ## Buttons
        self.buttonframe = tk.Frame(self)
        self.buttonframe.grid(row=1, column=0, sticky="nesw")
        self.confirm_button  = tk.Button(self.buttonframe,
                                         text=Labels.BUTTON_OK,
                                         state=tk.DISABLED,
                                         command=self.confirm_tile)
        self.confirm_button.grid(column=0, sticky="w")
        self.has_animation_checkbutton = tk.Checkbutton(self.buttonframe,
                                                        text=Labels.BUTTON_HAS_ANIMATION,
                                                        variable=self.has_animation,
                                                        onvalue="has_animation",
                                                        offvalue="",
                                                        command=self.animationSubButtons
                                                        )
        self.has_animation_checkbutton.grid(column=0, sticky="w")
        self.has_seasons_checkbutton = tk.Checkbutton(self.buttonframe,
                                                      text=Labels.BUTTON_HAS_SEASONS,
                                                      state=tk.DISABLED,
                                                      variable=self.has_seasons,
                                                      onvalue="seasons",
                                                      offvalue="",
                                                      )
        self.has_seasons_checkbutton.grid(column=0, sticky="w")
        self.has_idle_checkbutton= tk.Checkbutton(self.buttonframe,
                                                  text=Labels.BUTTON_HAS_IDLE,
                                                  state=tk.DISABLED,
                                                  variable=self.has_idle,
                                                  onvalue="idle",
                                                  offvalue="",
                                                  )
        self.has_idle_checkbutton.grid(column=0, sticky="w")
        self.is_activator_checkbutton = tk.Checkbutton(self.buttonframe,
                                                       text=Labels.BUTTON_IS_ACTIVATOR,
                                                       variable=self.is_activator,
                                                       onvalue="is_animation",
                                                       offvalue="",
                                                       command=self.activatorSubButtons
                                                       )
        self.is_activator_checkbutton.grid(column=0, sticky="w")
        self.is_container_checkbutton = tk.Checkbutton(self.buttonframe,
                                                       text=Labels.BUTTON_IS_CONTAINER,
                                                       state=tk.DISABLED,
                                                       variable=self.is_container,
                                                       onvalue="is_container",
                                                       offvalue=""
                                                       )
        self.is_container_checkbutton.grid(column=0, sticky="w")
        self.is_door_checkbutton = tk.Checkbutton(self.buttonframe,
                                                  text=Labels.BUTTON_IS_DOOR,
                                                  state=tk.DISABLED,
                                                  variable=self.is_door,
                                                  onvalue="is_door",
                                                  offvalue="",
                                                  )

        self.is_door_checkbutton.grid(column=0, sticky="w")
        self.has_lock_checkbutton = tk.Checkbutton(self.buttonframe,
                                                   text=Labels.BUTTON_HAS_LOCK,
                                                   state=tk.DISABLED,
                                                   variable=self.has_lock,
                                                   onvalue="has_lock",
                                                   offvalue="",
                                                   )
        self.has_lock_checkbutton.grid(column=0, sticky="w")

    def confirm_tile(self):
        # Don't press this button unless a new tile is applied.
        self.confirm_button.config(state=tk.DISABLED)

        # give tile uniqe ID, raise ID pool by one.
        t1 = self.current_tileset.get("id")
        t2 = str(len(list(self.current_tileset.findall("tile"))))
        id_ = t1 + "." + t2
        self.tile_element.set("id", id_)
        # append tile to internal tilelist
        self.current_tileset.append(self.tile_element)
        self.main.main_tilelist._update()
        self.tile_canvas.delete("all")
        self.tile_element = None
        self.created = False
        self.current_tab.scrapSelection()

    def animationSubButtons(self):
        if self.has_animation.get():
            self.has_seasons_checkbutton.config(state=tk.NORMAL)
            self.has_idle_checkbutton.config(state=tk.NORMAL)

        else:
            self.has_seasons_checkbutton.deselect()
            self.has_idle_checkbutton.deselect()
            self.has_seasons_checkbutton.config(state=tk.DISABLED)
            self.has_idle_checkbutton.config(state=tk.DISABLED)

    def activatorSubButtons(self):
        if self.is_activator.get():
            self.is_container_checkbutton.config(state=tk.NORMAL)
            self.is_door_checkbutton.config(state=tk.NORMAL)
            self.has_lock_checkbutton.config(state=tk.NORMAL)
        else:
            self.is_container_checkbutton.deselect()
            self.is_container_checkbutton.config(state=tk.DISABLED)
            self.is_door_checkbutton.deselect()
            self.is_door_checkbutton.config(state=tk.DISABLED)
            self.has_lock_checkbutton.deselect()
            self.has_lock_checkbutton.config(state=tk.DISABLED)

    def drawTileFromElement(self):
        pass

    def drawImages(self, image):
        self.tile_canvas.create_image(0,0, image=image, anchor=tk.NW)
        self.tile_image = image





