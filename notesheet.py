from pandaeditor import *
from notesection import NoteSection
import time

scroll_sensitivity = 5
pan_sensitivity = 1

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()
        self.name = 'notesheet'
        self.model = 'quad'
        self.texture = 'white_cube'

        self.scale = (256, 64)
        self.texture_scale = (self.scale_x, self.scale_y)

        self.color = color.gray
        self.origin = (-.5, -.5)
        self.collider = 'box'

        self.highlight = Entity(
            model = 'quad',
            origin = (-.5, -.5),
            color = color.color(90, 1, 1, .3),
            z = -.1
            )
        self.highlight.reparent_to(self)

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
        self.create_note_section(0, 0)

        self.playing = False
        self.recording = False
        self.start_time = time.time()
        self.indicator_start_x = self.indicator.x


    def new_project(self):
        if self.note_sections:
            print("warning")
        for ns in self.note_sections:
            ns.die()
        self.self.note_sections.clear()

        # tempoTapper.tempo = 60


    def input(self, key):
        if key == 'scroll down':
            camera.fov += scroll_sensitivity
        if key == 'scroll up':
            camera.fov -= scroll_sensitivity

        if key == 'space':
            if self.recording:
                self.stop_recording()
            elif not self.playing:
                self.play()
            else:
                self.stop()

        if key == 'double click' and self.hovered:
            self.create_note_section(mouse.point[0], mouse.point[1])


    def play(self):
        self.indicator_start_x = self.indicator.x
        self.playing = True
        for ns in self.note_sections:
            invoke(ns.play, delay=ns.x)


    def create_note_section(self, x, y):
        ns = NoteSection()
        ns.x = int(x * self.scale_x)
        ns.y = int(y * self.scale_y)
        ns.z = -.1
        self.note_sections.append(ns)
        self.prev_selected = ns

        target_scale_y = ns.scale_y
        ns.scale_y = 0
        ns.animate_scale_y(target_scale_y)

    def update(self, dt):
        if self.playing:
            print(time.time() - self.start_time)
            self.indicator.x = self.indicator_start_x + (time.time() - self.start_time) / 4 / 4 / 2

        if self.hovered:
            self.highlight.x = int(mouse.point[0] * self.scale_x) / self.scale_x
            self.highlight.y = int(mouse.point[1] * self.scale_y) / self.scale_y


        # panning
        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio

            camera.x = max(camera.x, 0)
            camera.y = max(camera.y, 0)


if __name__ == '__main__':
    app = PandaEditor()
    camera.orthographic = True
    camera.fov = 10
    sheet = NoteSheet()
    app.run()
