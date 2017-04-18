from xml.etree.ElementTree import Element, SubElement, ElementTree


class ProjectTree:

    def __init__(self):
        self.path = None
        self.name = None
        self.root = Element("root")
        self.tilesets = SubElement(self.root, "tilesets")
        self.maps = SubElement(self.root, "maps")
#        self.tilesets.set("new_id", "0")

        self.tree = ElementTree(self.root)


class MapTree:

    def __init__(self):
        self.path = None
        self.name = None
        self.root = Element("map")
