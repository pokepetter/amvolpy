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
            # print('no notesheet')
        self.name = 'notesection'
        self.parent = scene
        # self.require_key = 'shift'
        # self.model = 'quad'
        self.origin = (-.5, -.5)
        # self.color = color.color(0, 0, .06)
        self.color = color.color(0,0,.1)
        self.highlight_color = color.tint(self.color, .05)

        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
        self.octave = 0

        self.note_parent = Entity(parent=self)
        self.fake_notes_parent = Entity(parent=self.note_parent)
        self.note_area = NoteArea(
            note_section = self,
            parent = self.note_parent,
            color = color.color(1, 1, 0, .2),
            origin = (-.5, -.5, .1)
            )
        self.play_button = PlayButton(note_section=self)
        self.end_button = EndButton(note_section=self)
        self.loop_button_end = LoopButton(note_section=self)
        self.outline = Grid(1, 1, parent=self, color=color.dark_gray, z=-.2, thickness=4)
        self.grid = Grid(
            4 * round(self.note_area.scale_x),
            16,
            parent = self.note_area,
            z = -2.2,
            color = color.tint(self.color, .1))

        self.sounds = list()
        self.playing = False

        # self.instrument = 'violin-n72'
        self.instrument = '0DefaultPiano_n48'
        self.attack = 0
        self.falloff = .5


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
            # self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
            # self.sound.set_play_rate((note.y * 8 * 1.05946309436))

            # s = Sequence()
            # # print('wait:',(note.x * 2), (note.y * 8 * 1.05946309436))
            # s.append(Wait((note.x * 2)))
            # # s.append(SoundInterval(self.sound))
            # s.append()
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
        print('stop notesection')
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
                      round(y * snapsettings.position_snap) / snapsettings.position_snap,
                      -1)
        self.draw_fake_notes()
        return n


    def play_note(self, i, volume=1):
        # todo find closest
        print('play note:', i)
        # sound = loader.loadSfx("0DefaultPiano_n48.wav")
        distance = 48 - i
        self.sounds.append(Audio(
            self.instrument,
            pitch = pow(1 / 1.05946309436, distance),
            volume = volume,
            i = i
            ))

    def stop_note(self, i):
        for s in self.sounds:
            if s.i == i:
                s.fade_out(duration=self.falloff)
                self.sounds.remove(s)


    def draw_fake_notes(self):
        if self.note_area.scale_x == 0:
            print('ERROR: note_area.scale_x == 0')
            self.note_area.scale_x = max(.25, self.note_area.scale_x)
            # return
        destroy(self.fake_notes_parent)
        self.fake_notes_parent = Entity(parent=self.note_parent)
        # print('loops:', self.scale_x / self.note_area.scale_x)

        # disable out of bounds notes
        for n in self.notes:
            n.enabled = n.x < self.note_area.scale_x

        # draw fake notes for loops
        for i in range(1, math.ceil(self.scale_x / self.note_area.scale_x)):
            for n in [n for n in self.notes if n.x < self.note_area.scale_x]:
                if n.x + (i * self.note_area.scale_x) >= self.scale_x:
                    break
                clone = FakeNote()
                clone.strength = n.strength
                clone.length = n.length
                clone.color = color.color(60, .5, .5, 1)
                clone.reparent_to(self.fake_notes_parent)
                clone.x = n.x + (i * self.note_area.scale_x)
                clone.y = n.y
                clone.z = -.1


    @property
    def notes(self):
        return [c for c in self.note_parent.children if c.type == 'Note']


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

    def on_click(self):
        if held_keys['control']:
            self.note_section.add_note(mouse.point[0], mouse.point[1])

    def input(self, key):
        if key == 'control':
            # show self so I can place notes
            self.z = 0
            self.note_section.grid.z += 2

        elif key == 'control up':
            self.z = 2
            self.note_section.grid.z -= 2




if __name__ == '__main__':
    app = Ursina()
    window.color = color.color(0, 0, .12)
    camera.orthographic = True
    camera.fov = 10

    t = NoteSection()
    t.add_note(0, 1/16)
    t.add_note(.25, 2/16)
    t.add_note(.5, 3/16)
    t.add_note(.75, 2/16)
    app.run()
