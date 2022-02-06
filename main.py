from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from utils import *

app = Ursina(vsync = getConfig("VSYNC"))

# Game Variables
window.fps_counter.color = color.black
VSYNC = 'On' if getConfig('VSYNC') else 'Off'
ingameentities = {}

def resumeM(currentities):
    for i in currentities:
        destroy(currentities[i])
    window.color = color.white
    mouse.locked = True
    

def pauseMenu():
    mouse.locked = False
    mainMenu = Button(text = "Main Menu", scale = (.5, .10, .25), position = (0, 0, 0), color = color.red, texture = "assets/ChineseButtonTexture")  
    resume = Button(text = "Resume", scale = (.5, .10, .25), position = (0, .10, 0), color = color.red, texture = "assets/ChineseButtonTexture")
    mainMenu.on_mouse_enter, mainMenu.on_mouse_exit, resume.on_mouse_enter, resume.on_mouse_exit = Func(changeEntityColor, mainMenu, color.gray), Func(changeEntityColor, mainMenu, color.red), Func(changeEntityColor, resume, color.gray), Func(changeEntityColor, resume, color.red)
    window.color = color.black
    ingameentities = {
        "mainMenu": mainMenu,
        "resume": resume
    }
    resume.on_click = Func(resumeM, ingameentities)
    

# Classes
class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.posLabel = Text("", position = window.top_left, color = color.black)
    
    def update(self):
        super().update()
        self.posLabel.text = f"x: {round(self.x)} y: {round(self.y)} z: {round(self.z)}"
    
    def input(self, k):
        super().input(k)
        if k == "escape":
            pauseMenu()
    
    def update(self):
        if mouse.locked: super().update()
        else: pass
# Functions (Not built-in)
changeEntityColor = lambda e, c: setattr(e, "color", c)

def mainGameplay(currentities):
    global ingameentities
    for i in currentities:
        destroy(currentities[i])
    sky = Sky()
    player = Player()
    player.position = (6.5, 3, 6.5)
    player.mouse_sensitivity = (getConfig("SENSITIVITY"), getConfig("SENSITIVITY"))
    player.speed = 12.5
    for x in range(15):
        Entity(model = "cube", position = (x, 1, 14), collider = "cube", texture = "brick", color = color.red)
        Entity(model = "cube", position = (x, 1, 0), collider = "cube", texture = "brick", color = color.red)
        for z in range(15):
            Entity(model = "cube", position = (14, 1, z), collider = "cube", texture = "brick", color = color.red)
            Entity(model = "cube", position = (0, 1, z), collider = "cube", texture = "brick", color = color.red)
            Entity(model = "cube", position = (x, 0, z), collider = "cube", texture = 'grass')
    ingameentities = {
        "player": player,
        "sky": sky
    }

def mainMenu(currentities):
    for i in currentities:
        destroy(currentities[i])
    background = Entity(
    model = "cube",
    scale = (15, 15, 15),
    texture = "assets/BackGround"
    )
    play = Button(text = "Play", scale = (.5, .10, .25), position = (0, .25, 0), color = color.red, texture = 'assets/ChineseButtonTexture')
    settings = Button(text = "Settings", scale = (.5, .10, .25), position = (0, .12, 0), color = color.red, texture = 'assets/ChineseButtonTexture')
    exit = Button(text = "Exit", scale = (.5, .10, .25), position = (0, -.1, 0), color = color.red, texture = 'assets/ChineseButtonTexture') 
    play.on_mouse_enter, settings.on_mouse_enter, exit.on_mouse_enter = Func(changeEntityColor, play, color.gray), Func(changeEntityColor, settings, color.gray), Func(changeEntityColor, exit, color.gray)
    play.on_mouse_exit, settings.on_mouse_exit, exit.on_mouse_exit = Func(changeEntityColor, play, color.red), Func(changeEntityColor, settings, color.red), Func(changeEntityColor, exit, color.red)
    exit.on_click = lambda: application.quit() if exit.visible else print("")
    settings.on_click = Func(settingsScreen, {
        "play": play,
        "settings": settings,
        "exit": exit,
        "background": background
    })  
    play.on_click = Func(mainGameplay, {
        "play": play,
        "settings": settings,
        "exit": exit,
        "background": background
    })
    ingameentities = {
        "play": play,
        "settings": settings,
        "exit": exit,
        "background": background
    }

def settingsScreen(currentities):
    for i in currentities:
        if i == "background": continue
        destroy(currentities[i])
    difficulity = DropdownMenuX(getConfig('DIFFICULITY'), buttons = (
        DropdownMenuButton('Easy', on_click = lambda: changeConfig("DIFFICULITY", "Easy")),
        DropdownMenuButton('Medium', on_click = lambda: changeConfig("DIFFICULITY", "Medium")),
        DropdownMenuButton('Hard', on_click = lambda: changeConfig("DIFFICULITY", "Hard"))
    ))
    vsync = DropdownMenuX(VSYNC, buttons = (
        DropdownMenuButton("On", on_click = lambda: changeConfig("VSYNC", True)),
        DropdownMenuButton("Off", on_click = lambda: changeConfig("VSYNC", False))
    ))
    sensitivity = Slider(50, 200, position = (-.1, .125, 0))
    sensitivity.value = getConfig("SENSITIVITY")
    sensitivity.on_value_changed = lambda: changeConfig("SENSITIVITY", round(sensitivity.value, 2))
    vsynclabel = Text("Vsync: ", position = (-.25, .075, 0), color = color.black)
    senslabel = Text("Sensitivity: ", position = (-.25, .140, 0), color = color.black)
    difflabel = Text("Difficulity: ", position = (-.25, 0, 0), color = color.black)
    vsync.position = (-.1, .075, 0)
    difficulity.position = (-.1, 0, 0)
    backButton = Button("Back", position = (window.top_left.x + .075, window.top_left.y - .025), texture = "assets/ChineseButtonTexture", scale = (.15, .05, .25), color = color.red)
    backButton.on_mouse_enter, backButton.on_mouse_exit = Func(changeEntityColor, backButton, color.gray), Func(changeEntityColor, backButton, color.red)

    ingameentities = {
        "sensitivity": sensitivity,
        "senslabel": senslabel,
        "vsync": vsync,
        "vsynclabel": vsynclabel,
        "difficulity": difficulity,
        "difflabel": difflabel,
        "backButton": backButton
    }
    backButton.on_click = Func(mainMenu, ingameentities)


# Initializing
window.borderless = False
window.exit_button.enabled = False
window.size = (1600, 1200)
window.color = color.white


# Entities

mainMenu(ingameentities)






app.run()