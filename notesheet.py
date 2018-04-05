from pandaeditor import *
from notesection import NoteSection

scroll_sensitivity = 5
pan_sensitivity = 1

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()

        self.model = 'quad'
        self.color = color.white33
        self.origin = (-.5, -.5)
        self.collider = 'box'
        self.scale *= 8

        self.highlight = Entity(
            model = 'quad',
            origin = (-.5, -.5),
            color = color.color(90, 1, 1, .3),
            z = -.1
            )
        self.highlight.reparent_to(self)

        self.selection = []
        self.prev_selected = None

        ns = NoteSection()
        ns.reparent_to(self)
        ns.x = 0
        ns.y = 0
        ns.z = -.1
        self.prev_selected = ns


    def input(self, key):
        if key == 'scroll down':
            camera.fov += scroll_sensitivity
        if key == 'scroll up':
            camera.fov -= scroll_sensitivity

    def on_click(self):
        ns = NoteSection()
        ns.reparent_to(self)
        ns.x = int(mouse.point[0] * 8) / 8
        ns.y = int(mouse.point[1] * 8) / 8
        ns.z = -.1
        self.prev_selected = ns

    def update(self, dt):
        if self.hovered:
            self.highlight.x = int(mouse.point[0] * 8) / 8
            self.highlight.y = int(mouse.point[1] * 8) / 8

        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio


if __name__ == '__main__':
    app = PandaEditor()
    camera.orthographic = True
    camera.fov = 10
    sheet = NoteSheet()
    app.run()
