from pandaeditor import *

class Draggable(Entity):

    def __init__(self):
        super().__init__()

        self.model = 'quad'
        self.color = color.lime * .5 + color.white *.5
        self.collider = 'box'
        # self.parent = camera.ui

    def input(self, key):
        if key == 'scroll down':
            camera.fov += 5
            printvar(camera.fov)
        if key == 'scroll up':
            camera.fov -= 5
            printvar(camera.fov)

    def update(self, dt):
        if self.hovered and mouse.left:
            self.x += mouse.velocity[0] * camera.fov
            self.y += mouse.velocity[1] * camera.fov



if __name__ == '__main__':
    app = PandaEditor()
    camera.orthographic = True
    bg = Entity(
        model = 'quad',
        collider = 'box',
        scale = (10,10),
        z = 1
        )
    e = Draggable()
    app.run()
