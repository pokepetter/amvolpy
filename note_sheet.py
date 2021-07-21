from ursina import *
import note_recorder

class NoteSheet(Entity):

    def __init__(self):
        super().__init__()
        self.name = 'notesheet'
        self.playing = False
        self.bg = Entity(
            parent = self,
            model='quad',
            # model = Grid(256, 64, thickness=5),
            # model = Quad(radius=.001, mode='line'),
            # texture = 'white_cube',
            scale = (256, 64),
            # texture_scale = (256, 64),
            color = color.dark_gray.tint(.10),
            origin = (-.5, -.5),
            collider = 'box',
            z=1,
            )

        self.grid = Entity(parent=self.bg, model=Grid(256, 64), origin=(-.5,-.5), color=hsv(0,0,1,.1), z=-.01)
        self.scroll_sensitivity = 1
        self.pan_sensitivity = 1
        # self.highlight = Entity(
        #     world_parent = self,
        #     model = Quad(mode='line', thickness=2),
        #     color = color.white33,
        #     origin = (-.5, -.5),
        #     z = -.2
        #     )


        self.indicator = Entity(
            parent=self.bg,
            model = Mesh(vertices=[(0,0,0), (0,1,0)], mode='line', thickness=4),
            color = color.red,
            z = -4,
            )

        self.note_sections = list()
        self.prev_selected = None

        self.recording = False
        self.start_time = time.time()
        self.indicator_start_x = self.indicator.x


    def clear(self):
        print('clear')
        # if self.note_sections:
        #     print("warning")
        # for ns in self.note_sections:
        #     destroy(ns)
        # self.note_sections.clear()

        # tempoTapper.tempo = 60
        return True


    def input(self, key):
        if key == 'scroll down':
            camera.fov *= 1.1
        if key == 'scroll up':
            camera.fov /= 1.1
            # if not held_keys['control']:
                # self.scale_x -= .1
                # self.scale_x = max(self.world_scale_x, .025)
                # self.scale_y -= .1
                # self.scale_y = max(self.scale_y, .025)

        # if key == 'scroll up':
        #     self.scale_x += .1
        #     self.scale_y += .1
            # self.bg.x = -self.indicator.x

        if key == 'space':
            if self.recording:
                self.stop_recording()
            elif not self.playing:
                self.play()
            else:
                self.stop()

        if key == 'double click' and self.bg.hovered:
            self.create_note_section(mouse.point[0]*self.bg.scale_x, mouse.point[1]*self.bg.scale_y)


        if key == 'left mouse up' and self.bg.hovered and mouse.delta_drag == Vec3():
            self.indicator.x = mouse.point[0]



    def play(self):
        self.indicator_start_x = self.indicator.x
        self.playing = True
        for ns in self.note_sections:
            invoke(ns.play, delay=ns.x)

    def stop(self):
        self.indicator.x = self.indicator_start_x
        if note_recorder.recording:
            note_recorder.stop_recording()

        self.playing = False
        for ns in self.note_sections:
            ns.stop()


    def create_note_section(self, x, y):
        # from note_section import NoteSection
        from note_section_grid import NoteSectionGrid as NoteSection
        ns = NoteSection()
        print('create note section')
        ns.x = int(x * self.scale_x)
        ns.y = int(y * self.scale_y)
        ns.z = -2
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
            camera.x -= mouse.velocity[0] * camera.fov * self.pan_sensitivity / camera.aspect_ratio
            camera.y -= mouse.velocity[1] * camera.fov * self.pan_sensitivity
            # camera.x = max(camera.x, camera.fov / 2 * camera.aspect_ratio * .9)
            # camera.y = max(camera.y, camera.fov / 2 * .9)


sys.modules[__name__] = NoteSheet()


if __name__ == '__main__':
    import time
    from ursina import *

    t = time.time()
    app = Ursina()
    print(time.time() - t)
    # import main
    camera.orthographic = True
    camera.fov = 6
    camera.x = max(camera.x, camera.fov / 2 * camera.aspect_ratio * .9)
    camera.y = max(camera.y, camera.fov / 2 * .9)
    # import note_sheet

    # from note_recorder import NoteRecorder
    # base.note_recorder = NoteRecorder()
    # NoteSection()
    # camera.fov = 10
    app.run()
