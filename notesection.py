from ursina import *
from note import Note, FakeNote
import snapsettings
from end_button import EndButton
from loop_button import LoopButton
from play_button import PlayButton
from instrument_panel import InstrumentPanel
import save


class NoteSection(Draggable):

    def __init__(self, **kwargs):
        super().__init__()
        try:
            base.notesheet.note_sections.append(self)
        except:
            pass
        self.name = 'notesection'
        self.parent = scene
        self.origin = (-.5, -.5)
        self.color = color.color(0,0,.1)
        self.highlight_color = color.tint(self.color, .05)

        self.note_parent = Entity(parent=self)
        self.fake_notes_parent = Entity(parent=self.note_parent)
        self.note_area = NoteArea(
            note_section = self,
            parent = self.note_parent,
            color = color.color(1, 1, 0, .2),
            origin = (-.5, -.5, .1),
            scale_y = 4,
            )
        self.play_button = PlayButton(note_section=self)
        self.end_button = EndButton(note_section=self)
        self.loop_button_end = LoopButton(note_section=self)
        self.outline = Entity(model=Grid(1, 1), parent=self, color=color.dark_gray, z=-.2, thickness=4)
        self.grid = Entity(
            model=Grid(4 * round(self.note_area.scale_x), 32),
            parent = self.note_area,
            z = -2.2,
            color = color.tint(self.color, .1),
            y = (1/32/2),
            scale_y = 1/4
            )

        self.border = Entity(
            parent = self.note_area,
            model = Quad(subdivisions=0, mode='lines', thickness=2),
            z = -10,
            origin=(-.5,-.5),
            enabled = False
            )
        # self.border = Entity(parent=self.note_area, model=Quad(), z=-3, origin=(-.5,-.5))
        self.instrument_panel = InstrumentPanel(note_section=self)
        self.overlays = dict()

        self.sounds = list()
        self.playing = False
        self.octave = 0
        # self.instrument = 'samples/UoIowaPiano_n48'
        self.instrument = 'samples/0DefaultPiano_n48'
        self.attack = 0
        self.falloff = 4


    def input(self, key):
        super().input(key)

        if self.hovered or self.note_area.hovered:
            if key == 'c':
                self.crop()


        # redraw after deleting note
        if key == 'right mouse up':
            self.draw_fake_notes()

        if self.hovered or self.note_area.hovered:
            if key == 'delete':
                destroy(self)

        # selecting
        if key == 'left mouse down':
            if not held_keys['shift']:
                if self.hovered and hasattr(base, 'notesheet'):
                    for ns in base.notesheet.note_sections:
                        ns.selected = False

                    self.selected = True
                else:
                    self.selected = False


    def drag(self):
        self.end_button.reparent_to(self)

    def drop(self):
        self.x = round(self.x * 4) / 4
        self.y = round(self.y)
        self.end_button.reparent_to(self.parent)



    def crop(self):
        print('crop')
        for n in self.notes:
            if n.world_x - self.x < 0 or n.world_x >= self.x + self.scale_x:
                destroy(n)

    def play(self):
        self.playing_notes = list()
        self.sounds = list()

        for note in [n for n in (self.note_parent.children + self.fake_notes_parent.children) if n.type == 'Note']:
            note_num = int(note.y * 16) + (self.octave * 16)
            note_num = base.scalechanger.note_offset(note_num)

            s = invoke(self.play_note, note_num, delay=note.x)
            self.playing_notes.append(s)
            s = invoke(self.stop_note, note_num, delay=note.x+note.length)
            self.playing_notes.append(s)

        print('stop after:', self.scale_x)
        s = invoke(self.stop, delay=self.scale_x)
        self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()

        self.playing = True


    def stop(self):
        if self.playing:
            # print('stop notesection')
            for s in self.playing_notes:
                s.finish()
            self.playing = False


    def add_note(self, x=0, y=0, strength=1, length=1/4):
        print('adding note at: ', x, y)
        x *= self.note_area.scale_x
        n = Note()
        n.length = length
        n.reparent_to(self.note_parent)
        n.position = (round(x * snapsettings.position_snap) / snapsettings.position_snap,
                      round(y/128 * snapsettings.position_snap) / snapsettings.position_snap,
                      -1)
        self.draw_fake_notes()
        return n


    def play_note(self, i, volume=1, show_overlay=False):
        # todo find closest
        # print('play note:', i)
        # sound = loader.loadSfx("0DefaultPiano_n48.wav")
        if show_overlay:
            self.overlays[str(i)] = Entity(
                parent = self,
                model  ='quad',
                origin = (-.5,-.5),
                color = color.white66,
                y = i/64,
                z = -2,
                scale_y = 1/32
                )
            # destroy(particle, .2)

        distance = self.sample_note - i
        a = Audio(self.instrument, pitch=pow(1 / 1.05946309436, distance), volume=0, i=i)
        a.fade_in(value=volume, duration=self.attack, curve='linear')
        self.sounds.append(a)

    def stop_note(self, i):
        for s in self.sounds:
            if s.i == i:
                # print('stop note:', i)
                s.fade_out(duration=self.falloff, curve='linear')
                self.sounds.remove(s)

                if str(i) in self.overlays:
                    destroy(self.overlays[str(i)])


    def draw_fake_notes(self):
        if self.note_area.scale_x == 0:
            print('ERROR: note_area.scale_x == 0')
            self.note_area.scale_x = max(.25, self.note_area.scale_x)
            # return
        destroy(self.fake_notes_parent)
        self.fake_notes_parent = Entity(parent=self.note_parent,z=-1)
        # print('loops:', self.scale_x / self.note_area.scale_x)

        # disable out of bounds notes
        for n in self.notes:
            n.enabled = n.x < self.note_area.scale_x

        # draw fake notes for loops
        verts = list()
        for i in range(1, math.ceil(self.scale_x / self.note_area.scale_x)):
            for n in [n for n in self.notes if n.x <= self.note_area.scale_x]:
                if n.x + (i * self.note_area.scale_x) >= self.scale_x:
                    break

                verts.append((n.x + (i * self.note_area.scale_x), n.y, 0))
                verts.append((n.x + (i * self.note_area.scale_x) + n.length, n.y, 0))
                # clone.length = n.length
        self.fake_notes_parent.model = Mesh(vertices=verts, mode='line', thickness=5)
        self.fake_notes_parent.color = color.color(60, .5, .5, 1)
        points = duplicate(self.fake_notes_parent)
        points.parent = self.fake_notes_parent
        points.model.vertices = verts[::2]  # every other item
        points.model.mode = 'point'
        points.model.thickness = 10
        points.model.generate()



    @property
    def notes(self):
        return [c for c in self.note_parent.children if c.type == 'Note']

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

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.border.enabled = value


    def on_destroy(self):
        print('desrtoy')
        # destroy(self.end_button)
        self.end_button.reparent_to(self)
        base.notesheet.note_sections.remove(self)


class NoteArea(Button):
    def __init__(self, note_section, **kwargs):
        super().__init__(**kwargs)
        self.note_section = note_section
        self.highlight_color = self.color
        self.z = 2


    def input(self, key):
        if key == 'control':
            # show self so I can place notes
            self.z = 0
            self.note_section.grid.z += 2

        elif key == 'control up':
            self.z = 2
            self.note_section.grid.z -= 2

        if self.hovered and held_keys['control'] and key == 'left mouse up':
            self.note_section.add_note(mouse.point[0], mouse.point[1]*32)



class InstrumentPanel(Button):
    def __init__(self, note_section, **kwargs):
        super().__init__(**kwargs)
        self.note_section = note_section
        self.parent = note_section
        self.origin = note_section.origin
        self.color = color.white66
        self.highlight_color = self.color

    def input(self, key):
        self.z = -held_keys['left shift'] * 2
        # print(held_keys['left shift'])


if __name__ == '__main__':
    app = Ursina()
    from scalechanger import ScaleChanger
    app.scale_changer = ScaleChanger
    window.color = color.color(0, 0, .12)
    camera.orthographic = True
    camera.fov = 4

    t = NoteSection()
    t.add_note(0, 1)
    t.add_note(.25, 2)
    t.add_note(.5, 3)
    t.add_note(.75, 2)
    app.run()
