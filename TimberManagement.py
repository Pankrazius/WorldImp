from xml.etree.ElementTree import Element, SubElement, ElementTree, dump
from config import *

def newPreferenceTree():
    settings = Element("preferences")
    attribs = [("onStart", "new"),
               ("language", "english")]
    for attrib in attribs:
        settings.set(attrib[0], attrib[1])
    settings_tree = ElementTree(settings)
    return settings_tree


def newProjectTree():
    project = Element("project")
    project.set("name",  "")
    project.set("path",  "")
    project.set("project_path", "")
    project.set("filename", "")
    # todo: add further attributes
    tilesets = SubElement(project, "tilesets")
    tilesets.set("path", Paths.D_TILESETS)
    maps = SubElement(project, "maps")
    maps.set("path", Paths.D_MAPS)
    # todo: add further SubElements for other game-features like sound, items and stuff.
    project_tree = ElementTree(project)
    dump(project)
    return project_tree


def updateProjectTree(tag, name, id_):
    element = Element(tag)
    element.set("name", name)
    element.set("id", id_)
    return element


def newTileset(name, id_, source, path):
    tileset = Element("tileset")
    attribs = [("filename", name),
               ("id", id_),
               ("source", source),
               ("path", path),
               ("orient", ""),
               ("height", ""),
               ("width", ""),
               ("type", "tilesets")]
    for attrib in attribs:
        tileset.set(attrib[0], attrib[1])
    return tileset


def newMap():
    map = Element("map")
    map.set("name", "")
    map.set("id", "")
    return map


def newTile(tile):
    attribs = [("id", ""),
               ("name", ""),
               ("x", str(tile.rect.gx1)),
               ("y", str(tile.rect.gy1)),
               ("x_", str(tile.rect.gx2)),
               ("y_", str(tile.rect.gy2)),
               ("width", str(tile.tile_image.width())),
               ("height", str(tile.tile_image.height()))]
    tile = Element("tile")
    for a in attribs:
        tile.set(a[0], a[1])
    return tile


class ProjectTree:

    def __init__(self):
        self.path = None
        self.name = None
        self.root = Element("project")
        self.tilesets = SubElement(self.root, "tilesets")
        self.maps = SubElement(self.root, "maps")

        self.tree = ElementTree(self.root)



class MapTree:

    def __init__(self):
        self.path = None
        self.name = None
        self.root = Element("map")
