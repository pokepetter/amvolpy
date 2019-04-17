from ursina import *
from note import Note
from end_button import EndButton
from loop_button import LoopButton
from amvol_tooltip import AmvolTooltip as Tooltip
import scalechanger
import save_system
from ursina.prefabs.radial_menu import RadialMenu, RadialMenuButton


class NoteSection(Draggable):

    overlay_parent = Entity()
    overlay_index = 0
    for i in range(8):
        Entity(
            parent = overlay_parent,
            model  ='quad',
            origin = (-.5,-.5),
            color = color.white66,
            y = i/64,
            z = -2,
            scale_y = 1/32,
            enabled = False
            )


    def __init__(self, **kwargs):
        super().__init__(parent=scene, model='quad', color=color.color(random.uniform(0,360), .5, .6), z=-1)
        try:
            import notesheet
            self.world_parent = notesheet
        except:
            pass
        self.highlight_color = self.color
        self.origin = (-.5, -.5)

        self.notes = list()
        self.note_parent = Entity(parent=self, color=color.smoke, z=-.1, model=Mesh(vertices=(), mode='triangle', thickness=camera.fov*2))
        self.note_loops = Entity(parent=self.note_parent, color=self.color.tint(.3), z=-.1, model=Mesh(vertices=(), mode='triangle', thickness=camera.fov*2))
        self.loop_lines = Entity(parent=self, color=color.azure, z=-.1, model=Mesh(vertices=(), mode='line', thickness=camera.fov*.5))
        self.height = 32
        self.scale_y = self.height / 32
        self.grid = Entity(parent=self, model=Grid(1, self.height), z=-.1, color=color.white33, enabled=False)
        self.outline = Entity(parent=self, model=Quad(mode='line', segments=0), origin=(-.5,-.5), z=-1)
        self.scroll = 0
        self.scroll_speed = 5
        self.scroll_indicator = Entity(parent=self, model='quad', scale=(1/64, 1/16), color=color.gray, origin=(.5, -.5))
        self.loops = 1
        self.loop_number = Text(parent=self, text='1', origin=(.6, -.4), scale=(3,3/self.scale_y), color=color.white33, y=.1)
        self.end_button = EndButton(self)
        self.loop_button = LoopButton(self)
        # self.play_button = Button(parent=self.grid, text='>', scale=.1, color=color.azure, origin=(-.5,-.5), position=(0,1,-.1), tooltip=Tooltip('Play'))
        self.right_click_menu = RadialMenu(
            (
                RadialMenuButton(text='>', on_click=self.play),
                RadialMenuButton(text='x', on_click=self.stop, color=color.red, scale=.5),
            ),
            enabled=False
            )

        self.current_note = None
        self.indicator = Entity(parent=self, model=Mesh(vertices=((0,0,0),(0,1,0)), mode='lines'), color=color.yellow, z=-1)

        self.sounds = list()
        [setattr(e, 'selected', False) for e in scene.entities if 'NoteSection' in e.types]
        NoteSection.overlay_parent.parent = self
        self.selected = True

        self.playing = False
        self.octave = 0
        self.sample_note = 48
        self.instrument = 'samples/UoIowaPiano_n48'
        # self.instrument = 'samples/0DefaultPiano_n48'
        # self.instrument = 'samples/violin-n72'
        # self.instrument = 'samples/Sin-n60-f100-loop'
        self.attack = .0
        self.falloff = 1

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        if not held_keys['control']:
            super().update()

        if self.hovered and mouse.left and self.current_note:   # drag note length
            self.current_note.length = Note.default_length + mouse.delta[0] * 8
            self.current_note.length = int(self.current_note.length * 16) / 16
            self.draw_notes()


    def drop(self):
        self.y = math.floor(self.y)
        self.x = math.floor(self.x)

    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.grid.enabled = True

    def on_mouse_exit(self):
        # if mouse.hovered_entity == self.play_button:
        #     return

        super().on_mouse_exit()
        self.grid.enabled = False


    def input(self, key):
        super().input(key)
        if key == 'p':
            self.play()
        if key == 's':
            self.stop()

        if self.hovered and held_keys['control']:
            x = (mouse.point[0] / self.end_button.x) * self.scale_x / self.loops
            # adjust for clicking in a loop
            x -= math.floor(mouse.point[0] * self.loops) * (self.end_button.x * self.scale_x)

            y = math.floor(mouse.point[1] * self.height) + self.scroll

            if key == 'left mouse down':
                print('place note', x,y)
                self.current_note = Note(x,y)
                self.notes.append(self.current_note)
                self.draw_notes()

            if key == 'right mouse down':
                self.notes = [n for n in self.notes if n.y != y or n.x > x or n.x+n.length <= x]
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
            self.right_click_menu.enabled = True


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
        self.notes.append(Note(x, y, length, strength))


    def draw_notes(self):
        note_verts = list()
        loop_note_verts = list()
        loop_lines = list()
        width = self.end_button.x * self.scale_x
        note_height = 1/self.height

        for i in range(0, math.ceil(self.loops)):
            if i > 0 and self.loops > 1:
                loop_lines += ((i/self.loops,0,0), (i/self.loops,1,0))

            for n in self.notes:
                if (n.y >= self.scroll and n.y < self.height + self.scroll
                and n.x <= min(width, self.loop_button.x*self.scale_x)
                and (i / self.loops) + (n.x / self.loops / width)<= 1
                ):
                    y = (n.y/self.height)+(1/self.height/2)
                    line = (
                        ((i/self.loops) + (n.x/self.loops/width), y-note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + n.length/self.loops/width, y-note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width), y+note_height/2, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + n.length/self.loops/width, y+note_height/2, 0),
                        )
                    line = (line[0], line[1], line[2], line[2], line[1], line[3])

                    if i == 0:
                        note_verts += line
                    elif self.loops > 1:
                        loop_note_verts += line


        self.note_parent.y = -self.scroll / self.height

        for e, verts in zip(
                (self.note_parent, self.note_loops, self.loop_lines),
                (note_verts, loop_note_verts, loop_lines)
            ):
            e.enabled = bool(verts)
            e.model.vertices = verts
            e.model.generate()

        self.loop_number.text = round(self.loops, 1)
        self.loop_number.world_scale = 3



    def play(self):
        self.playing_notes = list()
        self.sounds = list()
        self.indicator.animate_x(1, duration=self.scale_x, curve=curve.linear)

        active_notes = [n for n in self.notes if n.x <= self.end_button.x * self.scale_x]

        for i in range(math.ceil(self.loops)):
            loop_delay = i * self.end_button.x * self.scale_x

            for note in active_notes:
                if note.x + loop_delay >= self.scale_x:
                    break

                note_num = scalechanger.note_offset(note.y)
                print(note_num, note.x)
                s = invoke(self.play_note, note_num, delay=note.x + loop_delay)
                self.playing_notes.append(s)
                s = invoke(self.stop_note, note_num, delay=note.x+note.length + loop_delay)
                self.playing_notes.append(s)

        print('stop after:', self.scale_x)
        s = invoke(self.stop, delay=self.scale_x)
        self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()

        self.playing = True


    def stop(self):
        if self.playing:
            print('stop notesection')
            self.indicator.x_animator.finish()
            self.indicator.x = 0
            for s in self.playing_notes:
                s.finish()
            self.playing = False


    def play_note(self, i, volume=1, show_overlay=False):
        # todo find closest
        # print('play note:', i)
        # sound = loader.loadSfx("0DefaultPiano_n48.wav")
        distance = self.sample_note - i
        a = Audio(self.instrument, pitch=pow(1 / 1.05946309436, distance), volume=0, i=i)
        a.fade_in(value=volume, duration=self.attack, curve=curve.linear)
        self.sounds.append(a)

        NoteSection.overlay_index += 1
        if NoteSection.overlay_index >= 8:
            NoteSection.overlay_index = 0

        if show_overlay:
            target_overlay = NoteSection.overlay_parent.children[NoteSection.overlay_index]
            target_overlay.y = i/64
            target_overlay.enabled = True


    def stop_note(self, i):
        for s in self.sounds:
            if s.i == i:
                # print('stop note:', i)
                s.fade_out(duration=self.falloff, curve=curve.linear)
                self.sounds.remove(s)

                for overlay in NoteSection.overlay_parent.children:
                    if int(overlay.y * 64) == i:
                        overlay.enabled = False


    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, value):
        self._instrument = value
        self.sample_note = 48
        # search for n followed by number to get the sample's note
        sample_info = self.instrument.split('_')
        for line in sample_info:
            if line.startswith('n'):
                if int(line[1:]):
                    # print('found start note:', int(line[1:]))
                    self.sample_note = int(line[:1])

    def __str__(self):
        notes = str([str(n) for n in self.notes]).replace('\'', '')
        return dedent(f'''
        {__class__.__name__}(
            instrument='{self.instrument}', attack={self.attack}, falloff={self.falloff},
            x={self.x}, y={int(self.y)}, scroll={self.scroll}, octave={self.octave}, size={self.size}, loops={self.loops},
            notes={notes},
            )
        ''')


if __name__ == '__main__':
    app = Ursina()
    from keyboard import Keyboard
    keyboard = Keyboard()
    camera.orthographic = True
    camera.fov = 4
    camera.position = (.5,.5)
    # note_section_parent = Entity()
    note_section = NoteSection(size=1, loops=1)
    note_section.selected = True

    for i, y in enumerate(range(24, 8, -8)):
        note_section.add_note(i/4, y, 1/4, 1)

    note_section.draw_notes()

    app.run()
