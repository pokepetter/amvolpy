from pandaeditor import *

class Draggable(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dragging = False

    def on_click(self):
        self.dragging = True

    def input(self, key):
        if key == 'left mouse up':
            self.dragging = False

    def update(self, dt):
        if self.dragging:
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
