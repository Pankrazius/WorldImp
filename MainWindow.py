from imports import *
from TileImp import TilesetFrame
from TileListFrame import TileListFrame
from MapImp import MapFrame
from pathlib import Path


class MainWindow(tk.Frame):
    """Contains all sub-modules packed in a notebook"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        ## Layout Stuff
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=15, minsize=80)
        self.columnconfigure(1, weight=85)
        self.main_tilelist = TileListFrame(self)
        self.main_tilelist.grid(row=0, column=0, sticky="nesw")
        self.main_notebook = ParentedNotebook(self)
        self.main_notebook.grid(row=0, column=1, sticky="nesw")
        ## Data Stuff
        self.check = "You are at MainWindow"
        self.tabs = [MapFrame(self),TilesetFrame(self)]
        #self.dummy_tree = ProjectTree()  # dummy. replace with function later.
        self.preferences = self._checkPreferences().getroot()
        self.project_tree = None
        self.widgets = {}
        self.trees = {} # Save the trees!
        self.images = {}
        ## Function Stuff
        self._loadProject()
        self._createNotebook()


    def newId(self, tag):
        if not self.project_tree == None:
            project = self.project_tree.getroot()
            return str(len(list(project.find(tag))) + 1)
        else:
            return False

    def _checkPreferences(self):
        """
        private methode of MainWindow

        opens preference-file, and load preferences
        creates empty preference file on first start.

        """
        pref_path = Path(os.getcwd()+"/preferences.xml")
        print(pref_path)
        if pref_path.is_file():
            pass
        else:
            print("preference doesn't exist yet")
            newPreferenceTree().write("preferences.xml", encoding="utf-8", xml_declaration=True)
        pref_tree = ElementTree()
        pref_tree.parse("preferences.xml")
        return pref_tree


    def _loadProject(self):
        """
        Private methode of MainWindow

        starts program depending on preferences.
        New = start a new ProjectTree
        Restore = open last ProjectTree
        Load = load specified ProjectTree
        """
        on_start = self.preferences.get("onStart")
        if on_start == "new":  # Pref.ON_Start
            print("Starting new Project")
            self.project_tree = newProjectTree()
            self.trees["project"] = self.project_tree
            npw = NewProjectWindow(self)
            self.widgets["npw"] = npw
        elif on_start == "restore":
            print("Restore last session")
            pass
        elif on_start == "load":
            print("load Project")
            pass
        else:
            print("Repent! The End is Nigh!")
            self.master.quit()

    def isInProjectPath(self, sourcepath):
        """returns if a file is inside the ProjectPath"""
        if self.project_tree:
            project = self.project_tree.getroot()
            project_path = os.path.join(os.getcwd(), project.get("path"))
            return sourcepath.startswith(project_path)
        else:
            print("Something's off!")

    def _createNotebook(self):
        for tabclass in self.tabs:
            tab = tabclass
            self.main_notebook.add(tab, text=tab.label)
            self.widgets[tab.label] = tab

    def saveProject(self, main_path=False):
        # ToDo: Make Save-Dialogue to save project in arbitrary folders
        """Writes ETrees to Disc"""
        project_path = self.project_tree.getroot().get("project_path")
        if not main_path:
            main_path = os.path.join(os.getcwd(), project_path)
        for tree in self.trees:
            root = self.trees[tree].getroot()
            if root.get("path"):
                tree_path = os.path.join(main_path,
                                         root.get("path"),
                                         root.get("filename"))
            else:
                tree_path = os.path.join(main_path,
                                         root.get("filename"))
            self.trees[tree].write(tree_path, encoding="utf-8", xml_declaration=True)

    def loadProject(self, initialdir=False):
        """
        Loads Project-Tree from file. Loads Sub-Trees accordingly
        Takes initialdir: a string defining a directory to init the filedialogue
        """
        options = {"filetypes": [("xml file", ".xml"), ("Imp Engine Project file", ".iep")], "initialdir": os.getcwd()}
        filename = tkfd.askopenfilename(**options)
        print(filename)









if __name__ == "__main__":

    root = tk.Tk()
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.minsize(int(Dims.WIN_MIN_SIZE[0]), int(Dims.WIN_MIN_SIZE[1]))
    app = MainWindow(root)
    root.mainloop()