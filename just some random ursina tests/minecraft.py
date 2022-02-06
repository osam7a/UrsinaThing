'''
Disclaimer: This solution is not scalable for creating a big world.
Creating a game like Minecraft requires specialized knowledge and is not as easy
to make as it looks.
You'll have to do some sort of chunking of the world and generate a combined mesh
instead of separate blocks if you want it to run fast. You can use the Mesh class for this.
You can then use blocks with colliders like in this example in a small area
around the player so you can interact with the world.
'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )


    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal)

            if key == 'left mouse down':
                destroy(self)


for z in range(8):
    for x in range(8):
        voxel = Voxel(position=(x,0,z))

class Player(FirstPersonController):
    def __init__(self):
        super().__init__(mouse_sensitivity = (125, 125))


player = Player()
window.borderless = False
window.size = (1500, 1100)
coords = Text(f"", position = window.top_left, color=color.black)
player.flight = True
player.cursor.model, player.cursor.scale = "sphere", (.001, .001, .001)
def input(k):
    if k == "escape":
        mouse.locked = not mouse.locked

def update():
        coords.text = f"x: {round(player.x)} y: {round(player.y)} z: {round(player.z)}"
        if player.y < -200:
            player.y, player.z, player.x = 200, 0, 0
        if held_keys['p']:
                player.y += time.dt*5

app.run()
 