from pandaeditor import *

scroll_sensitivity = 5
pan_sensitivity = 1

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()
        for y in range(10):
            for x in range(10):
                self.bg = Entity(
                    position = (x, y),
                    scale = (.95, .95),
                    model = 'quad',
                    # color = color.red,
                    # scale = (1024, 1024),
                    z = 1
                )


    def input(self, key):
        if key == 'scroll down':
            camera.fov += scroll_sensitivity
        if key == 'scroll up':
            camera.fov -= scroll_sensitivity

    def update(self, dt):
        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio
