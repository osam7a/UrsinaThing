from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu
from ursina.prefabs.first_person_controller import FirstPersonController
import json

def changeConfig(key, value):
    f = open("config.json", "r")
    load = json.load(f)
    load[key] = value
    f.close()
    f = open("config.json", "w")
    json.dump(load, f)
    f.close()

def getConfig(key):
    f = open("config.json", "r")
    load = json.load(f)
    f.close()
    return load[key]


class DropdownMenuX(DropdownMenu):
    def __init__(self, text='', buttons=list(), **kwargs):
        super().__init__(text, buttons, **kwargs)
        self.value = None

    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self):
            self.value = mouse.hovered_entity.text
            self.text = mouse.hovered_entity.text
            self.close()
