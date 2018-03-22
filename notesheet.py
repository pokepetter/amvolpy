from pandaeditor import *
from notesection import NoteSection

scroll_sensitivity = 5
pan_sensitivity = 1

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()

        # self.parent = camera.ui
        # self.scale *= .05
        for y in range(10):
            for x in range(10):
                self.bg = SheetSquare(
                    parent = self,
                    position = (x, y),
                    origin = (-.5, -.5),
                    scale = (.975, .975),
                    model = 'quad',
                    collider = 'box',
                    color = color.dark_gray,
                    # scale = (1024, 1024),
                    z = 1
                )
                # self.bg.parent = self

        camera.x = 4
        camera.y = 4


    def input(self, key):
        if key == 'scroll down':
            camera.fov += scroll_sensitivity
        if key == 'scroll up':
            camera.fov -= scroll_sensitivity


    def update(self, dt):
        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio

class SheetSquare(Entity):
    # pass
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     # self.collider = 'box'
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def on_mouse_enter(self):
        self.color = color.lime

    def on_mouse_exit(self):
        self.color = color.dark_gray
    def input(self, key):
        if self.hovered and key == 'space':
            note_section = NoteSection()
            note_section.parent = self
            # note_section.position = self.position

if __name__ == '__main__':
    app = PandaEditor()
    sheet = NoteSheet()
    app.run()
