from xml.etree.ElementTree import Element, SubElement, ElementTree

class ProjectTree:

    def __init__(self, name):
        self.path = None
        self.name = name
        self.root = Element("root")
        self.tilesets = SubElement(self.root, "tilesets")
        self.tilesets.set("new_id", "0")
        self.tree = ElementTree(self.root)
