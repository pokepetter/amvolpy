from ursina import *
from note import Note
from end_button import EndButton
from loop_button import LoopButton
import instrument_loader
from instrument_menu import InstrumentMenu
from ursina.prefabs.radial_menu import RadialMenu, RadialMenuButton
import scale_changer
import math
# t = time.time()
# print(time.time() - t)

class NoteSection(Draggable):

    overlay_parent = None
    right_click_menu = None
    instrument_menu = None


    def __init__(self, **kwargs):
        super().__init__(parent=scene, model='quad', color=color.color(random.uniform(0,360), .5, .6), z=-1, step=(1/4, 1, 0))
        from main import note_sheet
        self.parent = note_sheet

        self.highlight_color = self.color
        self.origin = (-.5, -.5)

        self.height = 32

        if not NoteSection.overlay_parent:
            NoteSection.overlay_parent = Entity()
            NoteSection.overlay_index = 0
            for i in range(8):
                Entity(parent=NoteSection.overlay_parent, model='quad', origin=(-.5,-.5), color=color.white66, y=i/self.height, z=-2, scale_y=1/self.height, enabled=False, ignore=True)


        if not NoteSection.right_click_menu:
            NoteSection.radial_play_button = RadialMenuButton(text='>')
            NoteSection.radial_instrument_button = RadialMenuButton(text='inst', scale=.5)
            NoteSection.radial_destroy_button = RadialMenuButton(text='x', color=color.red, scale=.5)

            NoteSection.right_click_menu = RadialMenu(
                (
                NoteSection.radial_play_button,
                NoteSection.radial_instrument_button,
                NoteSection.radial_destroy_button,
                ),
                enabled=False
            )
        if not NoteSection.instrument_menu:
            NoteSection.instrument_menu = InstrumentMenu()

        self.notes = list()
        self.note_parent = Entity(parent=self, color=color.smoke, z=-.1, model=Mesh(vertices=list(), mode='triangle', thickness=camera.fov*2))
        self.note_loops = Entity(parent=self.note_parent, color=self.color.tint(.3), z=-.1, model=Mesh(vertices=list(), mode='triangle', thickness=camera.fov*2))
        self.note_parent.point_renderer = Entity(parent=self.note_parent.parent, color=self.note_parent.color, texture='circle', z=-.1)
        self.note_loops.point_renderer = Entity(parent=self.note_loops.parent, color=self.note_loops.color, texture='circle', z=-.1)
        self.loop_lines = Entity(parent=self, color=color.azure, z=-.1, model=Mesh(vertices=[Vec3(0,0,0), Vec3(1,0,0)], mode='line', thickness=camera.fov*.5))
        self.scale_y = self.height / 32
        self.grid = Entity(parent=self, model=Grid(4,self.height), z=-1, origin=(-.5,-.5), color=color.color(0,0,1,.2), enabled=False)
        self.outline = Entity(parent=self, model=Quad(mode='line', segments=0, thickness=2), origin=(-.5,-.5), z=-1, enabled=False)
        self.scroll = 0
        self.scroll_speed = 5
        self.scroll_indicator = Entity(parent=self, model='quad', scale=(1/64, 1/16), color=color.gray, origin=(.5, -.5))
        self.loops = 1
        self.loop_number = Text(parent=self, text='1', origin=(.6, -.4), scale=(3,3/self.scale_y), color=color.white33, y=.1)
        self.end_button = EndButton(self, x=1)
        self.loop_button = LoopButton(self)
        # self.play_button = Button(parent=self.grid, text='>', scale=.1, color=color.azure, origin=(-.5,-.5), position=(0,1,-.1), tooltip=Tooltip('Play'))

        self.current_note = None
        self.indicator = Entity(parent=self, model=Mesh(vertices=((0,0,0),(0,1,0)), mode='line', thickness=3), color=color.white66, z=-1)

        self.sounds = list()
        self.samples = list()
        [setattr(e, 'selected', False) for e in scene.entities if isinstance(e, NoteSection)]
        NoteSection.overlay_parent.parent = self
        self.selected = True

        self.playing = False
        self.octave_offset = 0
        self.attack = .05
        # self.attack = .5
        self.falloff = .01
        self.speed = 1
        # self.sample_note = 48
        t = time.time()
        # self.instrument = '0_default_piano'main
        # print('.............', time.time() - t)
        # self.instrument = 'violin'
        self.instrument = 'uoiowa_piano'
        # self.instrument = 'Buffalo'
        # self.instrument = 'drum'
        # self.instrument = 'samples/Sin-n60-f100-loop'
        # self.instrument = 'oooooleander'
        # self.instrument = 'nujabes_drums_1'

        self.instrument_settings = Entity(parent=self, model='quad', color=color.black33, origin=(-.5,-.5), z=-.1, enabled=False)
        # instrument_button = Button(parent=self.instrument_settings, scale=(.9,.1), position=(.5,.9,-.1), text_origin=(-.45,0), text=self.instrument)
        # instrument_button.text_entity.world_scale = .15
        #
        #
        # instrument_button.on_click = open_instrument_menu
        # for c in self.children:
        #     if not c.collider:
        #         scene.entities.remove(c)
        print('|111111111', self in scene.entities)

        for key, value in kwargs.items():
            setattr(self, key, value)



    # @property
    # def selected(self):
    #     return self._selected
    #
    # @selected.setter
    # def selected(self, value):
    #     self._selected = value
    #     self.outline.enabled = value
    #     self.color = color.gray


    def update(self):
        # if held_keys['control']:
        #     super().update()

        if self.hovered and mouse.left and self.current_note:   # drag note length
            self.current_note.length = Note.default_length + mouse.delta[0] * 8
            self.current_note.length = int(self.current_note.length * 16) / 16
            self.draw_notes()

        self.end_button.world_scale = .075
        self.loop_button.world_scale_x = .075


    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.grid.enabled = True


    def on_mouse_exit(self):
        super().on_mouse_exit()
        self.grid.enabled = False


    def on_destroy(self):
        self.stop()


    def open_instrument_menu(self):
        print('opening insturment meniu', self)
        NoteSection.instrument_menu.target_note_section = self
        NoteSection.instrument_menu.enabled = True


    def input(self, key):
        # if self.dragging or not held_keys['control']:
            # super().input(key)

        if self.hovered:
            if key == 'left mouse down':
                # self.stop_dragging()
                x = (mouse.point[0] / self.end_button.x) * self.scale_x / self.loops
                # adjust for clicking in a loop
                x -= math.floor(mouse.point[0] * self.loops) * (self.end_button.x * self.scale_x)
                y = math.floor(mouse.point[1] * self.height) + self.scroll

                x = round_to_closest(x, 1/16)
                # print('place note', x,y)
                self.current_note = Note(x,y)
                self.notes.append(self.current_note)
                self.draw_notes()

            if key == 'left mouse up':
                self.current_note = None

            if key in ('arrow up', 'arrow up hold', 'scroll up'):
                self.scroll += self.scroll_speed
            if key in ('arrow down', 'arrow down hold', 'scroll down'):
                self.scroll -= self.scroll_speed

        if key == 'left mouse down':
            if not self.hovered and not held_keys['control']:
                self.selected = False
            else:
                self.selected = True
                NoteSection.overlay_parent.parent = self


        if self.hovered and key == 'right mouse down':
            NoteSection.right_click_menu.note_section = self
            NoteSection.right_click_menu.position = self.position
            NoteSection.radial_play_button.on_click = self.play
            NoteSection.radial_instrument_button.on_click = self.open_instrument_menu
            NoteSection.radial_destroy_button.on_click = Func(destroy, self)
            NoteSection.right_click_menu.enabled = True



    @property
    def duration(self):
        return self.scale_x / self.speed    # * bmp/60

    @property
    def size(self):
        return self.end_button.x * self.scale_x

    @size.setter
    def size(self, value):
        self.end_button.x = value

    @property
    def loops(self):
        return self.loop_button.x / self.end_button.x

    @loops.setter
    def loops(self, value):
        self.loop_button.x = self.end_button.x * value
        self.loop_button.drop()

    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value):
        value = clamp(value, 0, 128-self.height)
        self._scroll = value
        self.draw_notes()
        self.scroll_indicator.text = str(value)
        t = value/128 * 2
        self.scroll_indicator.y = lerp(0, 1-self.scroll_indicator.scale_y, t)
        # print(self.scroll_indicator.y)

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self.overlay.enabled = value


    def add_note(self, x, y, length=1/4, strength=1):
        return self.notes.append(Note(x, y, length, strength))


    def draw_notes(self):
        # self.note_parent.model.clear()
        note_verts = list()
        loop_note_verts = list()
        point_verts = list()
        # loop_lines = list()
        width = self.end_button.x * self.scale_x
        note_height = 1/self.height/4
        # self.note_parent.model.vertices.append((0,0,0), (1,0,0))
        self.grid.scale_x = self.end_button.x
        self.grid.model = Grid(self.size*16, self.height)
        self.grid.origin = self.origin

        for i in range(0, math.ceil(self.loops)):
            if i > 0 and self.loops > 1:
                self.loop_lines.model= Grid(self.loops, 1)
                self.loop_lines.origin = (-.5,-.5)

            self.note_parent.model.vertices.extend(((0,0,0), (1,0,0)))
            for j, n in enumerate(self.notes):
                if (n.y >= self.scroll and n.y < self.height + self.scroll
                and n.x <= min(width, self.loop_button.x*self.scale_x)
                and (i / self.loops) + (n.x / self.loops / width)<= 1
                ):
                    y = (n.y/self.height)+(1/self.height/2)


                    line = (
                        ((i/self.loops) + (n.x/self.loops/width) + 1/32/self.loops/width, y-note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + n.length/self.loops/width, y-note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + 1/32/self.loops/width, y+note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + n.length/self.loops/width, y+note_height/2, 0),
                        )
                    # self.note_loops.model.triangles.append([(j*4)+i for i in range(4)])
                    line = (line[0], line[1], line[2], line[2], line[1], line[3])

                    point = (
                        ((i/self.loops) + (n.x/self.loops/width) + 0, y, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + 1/32/self.loops/width, y-note_height*2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + 1/16/self.loops/width, y, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + 1/32/self.loops/width, y+note_height*2, 0),
                        )
                    line += (point[0], point[1], point[2], point[2], point[3], point[0])

                    if i == 0:
                        note_verts.extend(line)
                    elif self.loops > 1:
                        loop_note_verts.extend(line)


        self.note_parent.y = -self.scroll / self.height

        for e, verts in zip(
                (self.note_parent, self.note_loops),
                (note_verts, loop_note_verts)
            ):
            e.enabled = bool(verts)
            e.model.vertices = verts
            e.model.generate()

        self.loop_number.text = round(self.loops, 1)
        self.loop_number.world_scale = 3


    def play(self):
        if self.playing:
            self.stop()
            return

        print('-------------', self.speed)
        self.indicator.x = 0
        self.indicator.animate_x(1, duration=self.scale_x / self.speed, curve=curve.linear)
        NoteSection.radial_play_button.text = 'stop'
        active_notes = [n for n in self.notes if n.x <= self.end_button.x * self.scale_x]

        # print('-------------', self.loops)
        self.note_sequences = list()
        for i in range(math.ceil(self.loops)):
            loop_delay = i * self.end_button.x * self.scale_x

            for note in active_notes:
                if note.x + loop_delay >= self.scale_x:
                    break

                note_num = scale_changer.note_offset(note.y)
                self.note_sequences.append(
                    Sequence(
                        Wait((note.x / self.speed) + loop_delay / self.speed),
                        Func(self.play_note, note_num, original_note=note.y, duration=note.length / self.speed),
                        Wait(note.length / self.speed),
                        Func(self.stop_note, note_num, original_note=note.y)
                    )
                )
        self.stop_sequence = invoke(self.stop, delay=self.duration)

        for s in self.note_sequences:
            s.start()
        self.stop_sequence.start()

        self.playing = True
        print('started playing')


    def stop(self, force_stop=True):
        print('stop notesection')
        if not self.playing:
            return
            print('stop notesection error')

        self.indicator.x_animator.kill()
        self.indicator.x = 0
        NoteSection.radial_play_button.text = '>'

        if force_stop:
            for s in self.sounds:
                s.stop(destroy=True)

        for s in self.note_sequences:
            s.pause()
            s.kill()

        self.stop_sequence.kill()

        self.playing = False


    def play_note(self, i, volume=1, show_overlay=False, original_note=None, duration=None):
        if not self.samples:
            print('samples not found')
            return

        # print('play note:', original_note)
        i += (12 * self.octave_offset)
        # a = Audio(sound_file_name=loader.loadSfx(self.samples[i][0]), pitch=self.samples[i][1], volume=1, i=original_note, parent=self)
        a = Audio(sound_file_name=self.samples[i][0], pitch=self.samples[i][1], volume=1, i=original_note, parent=self)
        # a = Audio(self.instrument, pitch=pow(1 / 1.05946309436, distance), volume=0, i=i)
        attack = lerp(self.attack*2, self.attack, volume)
        if self.attack <= .01:
            attack = lerp(.1, self.attack, volume)
        a.fade_in(value=volume, duration=attack, curve=curve.linear)
        self.sounds.append(a)

        # if duration:
        #     # a.animate('volume', 0, duration=self.falloff, delay=duration)
        #     # destroy(a, delay=duration+self.falloff)
        #     # invoke(a.stop, delay=duration)
        #     # destroy(a, delay=duration)
        #     a.fade_out(duration=self.falloff, delay=duration)

        NoteSection.overlay_index += 1
        if NoteSection.overlay_index >= 8:
            NoteSection.overlay_index = 0

        if show_overlay and original_note:
            # print('------------', NoteSection.overlay_index, len(NoteSection.overlay_parent.children))
            target_overlay = NoteSection.overlay_parent.children[NoteSection.overlay_index]
            target_overlay.scale_y = 1 / self.height
            target_overlay.y = original_note / self.height
            target_overlay.enabled = True


    def stop_note(self, i, original_note=None):
        if not original_note:
            return
        for s in self.sounds:
            if s.i == original_note:
                # print('stop note:', original_note)
                s.fade_out(duration=self.falloff, curve=curve.linear, interrupt='kill')
                s.animate('volume', 0, duration=self.falloff, curve=curve.linear)
                self.sounds.remove(s)


                for overlay in NoteSection.overlay_parent.children:
                    if int(overlay.y * self.height) == original_note:
                        overlay.enabled = False


    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, name):
        # print('trying to load instrument:', name)

        for s in [e for e in self.children if isinstance(e, Audio)]:
            s.stop(destroy=True)
        self._instrument = name
        self.samples = instrument_loader.load_instrument(name, self)
        # self.attack =
        # self.falloff =
        print(f'set instrument: {name}, attack:{self.attack}, falloff:{self.falloff}')



    def __str__(self):
        notes = str([str(n) for n in self.notes]).replace('\'', '')
        return dedent(f'''
        {__class__.__name__}(
        instrument='{self.instrument}', attack={self.attack}, falloff={self.falloff},
            x={self.x}, y={int(self.y)}, scroll={self.scroll}, octave_offset={self.octave_offset}, size={self.size}, loops={self.loops},
            notes={notes},
            )
        ''')


if __name__ == '__main__':
    from ursina import *
    app = Ursina()
    # import main
    # import scale_changer
    import keyboard
    # Button.color =  color.color(22,.48,.42)
    # import keyboard
    # camera.orthographic = True
    # camera.fov = 4
    # camera.position = (.5,.5)
    # note_section_parent = Entity()
    camera.orthographic = True
    t = time.time()
    note_section = NoteSection(size=1, loops=1)
    note_section.selected = True
    print('----', time.time() - t)
    camera.fov = 2

    for i, y in enumerate(range(24, 8, -8)):
        note_section.add_note(i/4, y, 1/4, 1)

    note_section.draw_notes()

    app.run()
