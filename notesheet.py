from ursina import *
from note_section import NoteSection
import time
import sys


scroll_sensitivity = 1
pan_sensitivity = 1

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()
        self.name = 'notesheet'
        self.playing = False
        self.bg = Entity(
            parent = self,
            # model = 'quad',
            # model = Quad(radius=.001, mode='lines'),
            # texture = 'white_cube',
            scale = (256, 64),
            texture_scale = (256, 64),
            # color = window.color.tint(.10),
            origin = (-.5, -.5),
            collider = 'box'
            )
        # self.highlight = Entity(
        #     world_parent = self,
        #     model = Quad(mode='lines', thickness=2),
        #     color = color.white33,
        #     origin = (-.5, -.5),
        #     z = -.2
        #     )

        self.indicator = Entity(
            model = 'quad',
            color = color.white66,
            parent = self,
            scale_x =1 / self.scale_x * .02,
            z = .1,
            origin = (-.5, -.5)
            )

        self.note_sections = list()
        self.prev_selected = None

        self.recording = False
        self.start_time = time.time()
        self.indicator_start_x = self.indicator.x


    def new_project(self):
        if self.note_sections:
            print("warning")
        for ns in self.note_sections:
            destroy(ns)
        self.note_sections.clear()

        # tempoTapper.tempo = 60


    def input(self, key):
        # if key == 'scroll down':
        #     camera.fov += scroll_sensitivity
        # if key == 'scroll up':
        #     camera.fov -= scroll_sensitivity

        if key == 'scroll down':
            self.scale_x -= .1
            self.scale_x = max(self.scale_x, .1)
        if key == 'scroll up':
            self.scale_x += .1

        if key == 'space':
            if self.recording:
                self.stop_recording()
            elif not self.playing:
                self.play()
            else:
                self.stop()

        if key == 'double click' and self.bg.hovered:
            self.create_note_section(mouse.point[0]*self.bg.scale_x, mouse.point[1]*self.bg.scale_y)


    def play(self):
        self.indicator_start_x = self.indicator.x
        self.playing = True
        for ns in self.note_sections:
            invoke(ns.play, delay=ns.x)

    def stop(self):
        self.indicator.x = self.indicator_start_x
        self.playing = False
        for ns in self.note_sections:
            ns.stop()


    def create_note_section(self, x, y):
        ns = NoteSection()
        ns.x = int(x * self.scale_x)
        ns.y = int(y * self.scale_y)
        ns.z = -.1
        # self.prev_selected = ns

        target_scale_y = ns.scale_y
        ns.scale_y = 0
        ns.animate_scale_y(target_scale_y)
        return ns

    def update(self):
        if self.playing:
            # print(time.time() - self.start_time)
            self.indicator.x = self.indicator_start_x + (time.time() - self.start_time) / 4 / 4 / 2



        # panning
        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio

            camera.x = max(camera.x, 0)
            camera.y = max(camera.y, 0)


sys.modules['notesheet'] = NoteSheet()

if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    camera.orthographic = True
    # camera.fov = 10
    # sheet = NoteSheet()
    app.run()
