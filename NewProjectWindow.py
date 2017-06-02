from imports import *

class NewProjectWindow(object):

    def __init__(self, master):
        ## Data Stuff
        self.master = master
        self.window = tk.Toplevel(master)
        self.master.widgets["npt"]= self.window
        self.project_tree = master.project_tree.getroot()
        self.name = tk.StringVar()
        self.name.set(self.project_tree.get("name"))
        self.path = tk.StringVar()
        self.path.set(self.project_tree.get("path"))
        ## Layout stuff
        self.name_entry = tk.Entry(self.window, textvariable=self.name)
        self.name_label = tk.Label(self.window, text="Name")
        self.path_entry = tk.Entry(self.window, textvariable=self.path)
        self.path_label = tk.Label(self.window, text="Path")

        self.destroy_button = tk.Button(self.window, text=Labels.BUTTON_OK, command = self.create)
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.path_label.grid(row=1, column=0)
        self.path_entry.grid(row=1, column=1)
        self.destroy_button.grid(row=2, columnspan=2)

    def create(self):
        """
        A bit more than a dummy Function

        needs further checks and the abbility to rename directories.
        """
        if not self.name.get():
            print("kein Projekname angegeben!")
            return

        self.project_tree.set("name", self.name.get())

        if not self.path.get():
            print("kein Pfadname angegeben!")
            return
        elif self.path.get():
            rootdir = os.getcwd()
            basedir = self.path.get()
            defaultfolders = [Paths.D_IMAGES,
                              Paths.D_TILESETS,
                              Paths.D_DIALOGUE,
                              Paths.D_MAPS,
                              Paths.D_SOUNDS,
                              Paths.D_SCRIPTS]
            path = os.path.join(rootdir, basedir)
            os.mkdir(path)
            for f in defaultfolders:
                os.mkdir(os.path.join(path, f))

        self.project_tree.set("project_path", self.path.get())
        self.project_tree.set("filename", "project.xml")
        self.project_tree.set("path", "")
        del self.master.widgets["npt"]
        self.window.destroy()









