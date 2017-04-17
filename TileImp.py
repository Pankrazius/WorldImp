from imports import *


class TilesetFrame(tk.Frame):

    def __init__(self, top):
        tk.Frame.__init__(self, top)
        self.grid(row=0, column=0, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = Labels.MAIN_LABEL_TILESET
        self.top = top
        self.tile_editor = TileEditorFrame(self)
        self.tile_editor.config(bd=1, relief=tk.SUNKEN)
        self.tile_editor.place(relx=0, rely=0, relwidth=0.2, relheight=1.0)
        self.tileset_nb = ParentedNotebook(self)
        self.tileset_nb.place(relx=0.2, rely=0, relwidth=0.8, relheight=1.0)
        self._createTab()

    def _createTab(self):
        """Private Methode of TilesetFrame, creates new TabFrame in TilesetFrame.nb"""
        page = TabFrame(self.tileset_nb)
        self.tileset_nb.add(page, text=Labels.TILESET_NB_NEW)

    def _getTab(self):
        """Private Methode of TilesetFrame, returns the actual selected TabFrame-Object"""
        key = self.tileset_nb.select().split(".")[-1]
        return self.tileset_nb.children[key]

    def loadImage(self):
        options = {"filetypes": [("PNG image", ".png"), ("JPEG image", ".jpg")], "initialdir": Paths.DEFAULT_LOAD}
        filename = tkfd.askopenfilename(**options)
        if filename:
            tab = self._getTab()
            if tab.used is False:
                with open(filename, mode="rb") as file:
                    tab.imagepath = os.path.relpath(filename, os.getcwd())
                    tab.image = Image.open(filename)
                    tab.tkimage = ImageTk.PhotoImage(file=file)
                    self.tileset_nb.tab(tab, text=file.name.split("/")[-1])
                    tab.canvas.create_image(0, 0, image=tab.tkimage, anchor=tk.NW)
                    tab.canvas.config(scrollregion=(0, 0, tab.tkimage.width(), tab.tkimage.height()))
                    tab.used = True
                    tab.create_tileset_button.config(state=tk.NORMAL)
                    tab.canvas.bind("<ButtonPress-1>", tab._onButtonPress)
                    tab.canvas.bind("<B1-Motion>", tab._onMotionPress)
                    tab.canvas.bind("<ButtonRelease-1>", tab._onButtonRelease)
#                    tab.image.close()
                    self._createTab()
            else:
                print("Tab already in use, use new tab.")
        else:
            print("No file provided")




class TabFrame(tk.Frame):

    def __init__(self,top):
        tk.Frame.__init__(self,top)
        self.created = False
        self.grid(row=0, column=0, sticky="nesw")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.config(borderwidth=1, relief=tk.SUNKEN)
        self.top = top
        self.main = top.top.top
        self.used = False
        self.imagepath = None
        self.image = None
        self.tkimage = None
        self.rect = Rectangle(self)
        self.tree = None
        self.grid_lines = []
        self.ts_width = Dims.GRID_WIDTH
        self.ts_height = Dims.GRID_HEIGHT
        self.ts_lmargin = Dims.GRID_LMARGIN
        self.ts_tmargin = Dims.GRID_TMARGIN
        self.tss_width = tk.StringVar()
        self.tss_height = tk.StringVar()
        self.tss_lmargin = tk.StringVar()
        self.tss_tmargin = tk.StringVar()
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nesw")
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.buttonframe = tk.Frame(self, bd=1, relief=tk.RIDGE)
        self.buttonframe.grid(row=2, column=0, sticky="nesw")
        #Buttons
        self.create_tileset_button = tk.Button(self.buttonframe,
                                               text=Labels.BUTTON_CREATE_TS,
                                               state=tk.DISABLED,
                                               command=self.makeTileset
                                               )
        self.create_tileset_button.pack(side=tk.LEFT, anchor=tk.NW)
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
            self.rect.setup()

    def _getCell(self, x, y):
        return (x - self.ts_lmargin )// self.ts_width, (y - self.ts_tmargin) // self.ts_height

    def makeTile(self):
        cropped = self.image.crop((self.rect.gx1, self.rect.gy1, self.rect.gx2, self.rect.gy2))
        self.tile_image = ImageTk.PhotoImage(cropped)
        tile_editor = self.top.top.tile_editor
        if tile_editor.created is False:
            tile_editor.tile = OrderedDict()
            print(tile_editor.tile)
            tile_editor.tile_image = self.tile_image
            tile_editor.created = True
        tile_editor.tile["x"] = self.rect.gx1
        tile_editor.tile["y"] = self.rect.gy1
        tile_editor.tile["x_"] = self.rect.gx2
        tile_editor.tile["y_"] = self.rect.gy2
        tile_editor.tile["width"] = self.tile_image.width()
        tile_editor.tile["height"] = self.tile_image.height()
        tile_editor.current_tree = self.tree
        tile_editor.drawImages()
        tile_editor.confirm_button.config(state=tk.NORMAL)
        self.scrapSelection()

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

    def makeTileset(self):
        if self.created == False:
            make_tileset_tl = tk.Toplevel(self)
            self.main.widgets["make_tileset"] = make_tileset_tl
            labels = [
                      (Labels.TOOL_WIDTH, self.tss_width),
                      (Labels.TOOL_HEIGHT, self.tss_height),
                      (Labels.TOOL_LMARGIN, self.tss_lmargin),
                      (Labels.TOOL_TMARGIN, self.tss_tmargin)
                      ]
            frame = tk.Frame(make_tileset_tl)
            for label in labels:
                tk.Label(frame, text=label[0]).pack(side=tk.LEFT, anchor=tk.W)
                entry = tk.Entry(frame, width=Dims.TOOL_ENTRY_WIDTH, textvariable=label[1])
                entry.insert(0, str(label[1].get()))
                entry.pack(side=tk.LEFT)
            ok_button = tk.Button(make_tileset_tl, text=Labels.BUTTON_OK, command=self.confirmTileset)
            make_tileset_tl.grid()
            frame.grid(row=0, column=0, sticky="nesw")
            ok_button.grid(row=1, column=0)

        else: pass

    def confirmTileset(self):
        if self.tss_width.get() and self.tss_height.get() and self.tss_lmargin.get() and self.tss_tmargin.get():
            print(self.tss_width, self.tss_height, self.tss_lmargin, self.tss_tmargin)
            try:
                int(self.tss_width.get())
                int(self.tss_height.get())
                int(self.tss_lmargin.get())
                int(self.tss_tmargin.get())
            except:
                print("not an integer")
                return False
        else:
            print("values not given")
            return False
        if "confirm_button" not in self.main.widgets:
            confirm_button = tk.Toplevel(self)
            self.main.widgets["confirm_button"] = confirm_button
            text = tk.Label(confirm_button, text=Msg.ARE_YOU_SURE)
            ok_button = tk.Button(confirm_button, text=Labels.BUTTON_OK, command=self.setTileset)
            cancel_button = tk.Button(confirm_button, text=Labels.BUTTON_CANCEL, command=confirm_button.destroy)
            confirm_button.grid()
            text.pack()
            ok_button.pack()
            cancel_button.pack()
        else:
            pass

    def setTileset(self):
        id_ = self.newId()
        # build TilesetElement for ProjectTree
        project_ts = self.main.dummy_tree.root.find("tilesets")
        project_element = et.Element("tileset")
        project_element.set("id", id_)
        print(project_element.get("id"))
        project_element.set("file_path", self.imagepath.split(".")[0]+".tsx")
        project_ts.append(project_element)
        et.dump(project_ts)
        # build TilesetTree
        root = et.Element("root")
        ts_element = et.Element("tileset")
        ts_element.set("id", id_)
        print(ts_element.get("id"))
        ts_element.set("image_path", self.imagepath)
        ts_element.set("tile_width", self.tss_width.get())
        ts_element.set("tile_height", self.tss_width.get())
        ts_element.set("lmargin", self.tss_lmargin.get())
        ts_element.set("tmargin", self.tss_tmargin.get())
        root.append(ts_element)
        self.tree = et.ElementTree(root)
        # keep reference of TilesetTree
        self.main.main_tilelist.trees[ts_element.get("id")] = self.tree
        # close windows, update buttons
        self.main.widgets["confirm_button"].destroy()
        self.main.widgets["make_tileset"].destroy()
        del self.main.widgets["confirm_button"]
        del self.main.widgets["make_tileset"]
        self.create_tileset_button.config(state=tk.DISABLED)
        self.show_grid_button.config(state=tk.NORMAL)
        self.apply_button.config(state=tk.NORMAL)
        self.scrap_button.config(state=tk.NORMAL)
        self.created = True

    def newId(self):
        return str(len(list(self.main.dummy_tree.root.find("tilesets"))))


class TileEditorFrame(tk.Frame):
    """For editing single Tiles"""
    def __init__(self, top):
        tk.Frame.__init__(self, top)
        self.top = top
        self.main = self.top.top
        self.created = False
        self.tile_image = None
        self.tile = {}
        self.current_tree = None
        self.current_ts_id = None
        self.config(border=1, relief=tk.SUNKEN)
        self.tile_canvas = tk.Canvas(self)
        self.tile_canvas.place(relx=0, rely=0, relwidth=1.0, relheight=0.3)
        self.has_animation = tk.StringVar()
        self.has_seasons = tk.StringVar()
        self.has_idle = tk.StringVar()
        self.is_activator = tk.StringVar()
        self.is_container = tk.StringVar()
        self.is_door = tk.StringVar()
        self.has_lock = tk.StringVar()
        self.buttonframe = tk.Frame(self)
        self.buttonframe.place(relx=0, rely=0.3, relwidth=1.0, relheight=0.6)
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
        t1 = self.current_tree.find("tileset").attrib["id"]
        t2 = self.newId()
        print(t1, t2)
        self.tile["tid"] = t1 + "." + t2
        print(self.tile["tid"])
        # make Element from OrderedDict, pack Element in Tileset-Tree
        e = et.Element("tile")
        for item in self.tile.items():
            e.set(str(item[0]), str(item[1]))
        self.current_tree.find("tileset").append(e)
        # append tile to internal tilelist

        self.main.main_tilelist._update()

        self.tile_canvas.delete("all")
        self.tile.clear()
        self.created = False

    def newId(self):
        return str(len(list(self.current_tree.find("tileset"))))

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

    def drawImages(self):
        self.tile_canvas.create_image(0,0, image=self.tile_image, anchor=tk.NW)
        pass


