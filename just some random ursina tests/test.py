from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app=Ursina()

window.color=color.blue

ground = Entity(model='plane', collider='box', scale=100, texture='grass', texture_scale=(4,4))
wall01 = Entity(model='sphere', color=color.red, collider='box', scale=20, texture='brick', position=(0,20,50))
wall02 = Entity(model='sphere', color=color.red, collider='box', scale=20, texture='brick', position=(0,20,-50))
wall03 = Entity(model='sphere', color=color.red, collider='box', scale=20, texture='brick', position=(50,20,0))
wall04 = Entity(model='sphere', color=color.red, collider='box', scale=20, texture='brick', position=(-50,20,0))

player=FirstPersonController()

app.run()