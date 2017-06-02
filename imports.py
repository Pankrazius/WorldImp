import numpy as np
import os
import tkinter as tk
import tkinter.filedialog as tkfd
import xml.etree.ElementTree as et
from collections import OrderedDict
from config import Labels, Msg, Paths, Dims, Pref
from copy import copy
from itertools import product
from NewProjectWindow import *
from SpecialWidgets import ParentedNotebook, DynamicScrollbar, Rectangle
from TimberManagement import * #newProjectTree, newMap, newTileset, newTile, updateTilesets, newPreferenceTree, ProjectTree, MapTree
from PIL import ImageTk, Image
from tkinter import ttk







