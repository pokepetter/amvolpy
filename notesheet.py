from pandaeditor import *
from notesection import NoteSection, Header
from panda3d.core import TextureStage
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
        self.setTexScale(TextureStage.getDefault(), self.scale_x, self.scale_y)
        # self.setTexOffset(ts, -4, -2)
        self.set_texture = loader.load_texture('white_cube.png')

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
        self.selection = []
        self.prev_selected = None
        self.can_drag = False

        self.create_note_section(0, 0)

        self.playing = False
        self.recording = False
        self.start_time = time.time()
        self.indicator_start_x = self.indicator.x
        self.selection_text = Text(
            parent = camera.ui,
            position = (-.5 * window.aspect_ratio, .4)
            )
        self.selection_text.scale *= .1


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
            else:
                self.play()

        if key == 'left mouse down':
            # multiselect
            if isinstance(mouse.hovered_entity, Header):
                self.can_drag = True
                if not mouse.hovered_entity.parent in self.selection:
                    if not held_keys['shift']:
                        self.selection.clear()
                    self.selection.append(mouse.hovered_entity.parent)
                    # print('add to selection:', mouse.hovered_entity.parent)
            else:
                self.selection.clear()
                print('clear slecteion')

        if key == 'double click' and self.hovered:
            self.create_note_section(mouse.point[0], mouse.point[1])

        if key == 'left mouse up':
            self.can_drag = False
            for ns in self.selection:
                ns.x = round(ns.x * self.scale_x) / self.scale_x
                ns.y = round(ns.y * self.scale_y) / self.scale_y


        # if key == 'delete':
        #     self.delete_selected_note_sections()


    def play(self):
        self.indicator_start_x = self.indicator.x
        self.playing = True
        for ns in self.notesections:
            invoke(ns.play(), delay=ns.x)


    def clear_selection(self):
        for ns in self.note_sections:
            ns.selected = False
            self.selection = list()


    def create_note_section(self, x, y):
        ns = NoteSection()
        ns.reparent_to(self)
        ns.x = int(x * self.scale_x) / self.scale_x
        ns.y = int(y * self.scale_y) / self.scale_y
        ns.z = -.1
        self.note_sections.append(ns)
        self.prev_selected = ns
        self.clear_selection()
        self.selection.append(ns)
        ns.selected = True

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

        # dragging
        if mouse.left and self.can_drag:
            for ns in self.selection:
                try:
                    ns.world_x += mouse.velocity[0] * camera.fov
                    ns.world_y += mouse.velocity[1] * camera.fov
                except:
                    pass
                    print(ns, 'is not an Entity')

        # panning
        if mouse.middle:
            camera.x -= mouse.velocity[0] * camera.fov * pan_sensitivity
            camera.y -= mouse.velocity[1] * camera.fov * pan_sensitivity / window.aspect_ratio

            camera.x = max(camera.x, 0)
            camera.y = max(camera.y, 0)

        selection_string = '\n'.join([s.name for s in self.selection])
        self.selection_text.text = selection_string

if __name__ == '__main__':
    app = PandaEditor()
    camera.orthographic = True
    camera.fov = 10
    sheet = NoteSheet()
    app.run()
