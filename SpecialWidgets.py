## SpecialWidgets contains subclassed tkinter widgets and special purpose classes

import tkinter as tk
import tkinter.ttk as ttk

class ParentedNotebook(ttk.Notebook):
    """a basic ttk.Notebook with added 'top' attribute referring to parent"""

    def __init__(self, top):
        ttk.Notebook.__init__(self, top)
        self.top = top


class Rectangle(object):
    """Basic rectangle"""

    def __init__(self,parent):
        self.parent = parent
        self.rect = None
        self.set = False
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.gx1 = 0
        self.gx2 = 0
        self.gy1 = 0
        self.gy2 = 0
        self.width = 0
        self.height = 0

    def setup(self):
        self.gx1, self.gy1, self.gx2, self.gy2 = self.parent.canvas.bbox(self.rect)
        self.gx1 +=1; self.gy1 +=1; self.gx2 -=1; self.gy2 -=1
        self.set = True

    def center(self):
        return self.x1 + self.width/2, self.y1 + self.height/2

    def bcenter(self):
        return self.x1 + self.width/2, self.y1 + self.height

    def _reset(self):
        self.rect = None
        self.set = False
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        self.gx1 = 0
        self.gx2 = 0
        self.gy1 = 0
        self.gy2 = 0
        self.width = 0
        self.height = 0


