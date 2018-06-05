from pandaeditor import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait, SoundInterval
from note import Note
import snapsettings
from end_button import EndButton

class Grid(Entity):
    def __init__(self, w, h, **kwargs):
        super().__init__()

    pass

class NoteSection(Draggable):

    def __init__(self):
        super().__init__()

        self.name = 'notesection'
        self.parent = scene
        self.require_key = 'shift'
        # self.model = 'quad'
        self.origin = (-.5, -.5)
        # self.color = color.color(0, 0, .06)
        self.color = color.color(0,0,.1)
        self.highlight_color = color.tint(self.color, .05)

        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")

        self.note_parent = Entity(parent=self)
        self.loop_area = NoteArea(
            note_section = self,
            parent = self.note_parent,
            color = color.color(1, 1, 0, .2),
            origin = (-.5, -.5, .1)
            )
        # self.start_button = StartButton(note_section=self)
        self.end_button = EndButton(note_section=self)
        self.loop_button_end = LoopButton(note_section=self)
        self.outline = Grid(1, 1, parent=self, color=color.dark_gray, z=-.2, thickness=4)
        self.grid = Grid(
            4 * round(self.loop_area.scale_x),
            16,
            parent = self.loop_area,
            z = -.2,
            color = color.tint(self.color, .1))

        self.notes = list()


    def input(self, key):
        super().input(key)
        if key == 'space':
            self.play()

        if self.hovered and key == 'c':
            self.crop()

        # redraw after deleting note
        if key == 'right mouse up':
            self.draw_fake_notes()

    def drag(self):
        self.end_button.reparent_to(self)

    def drop(self):
        self.x = round(self.x * 4) / 4
        self.y = round(self.y)
        self.end_button.reparent_to(self.parent)



    def crop(self):
        for n in self.notes:
            if n.world_x - self.x < 0 or n.world_x >= self.x + self.scale_x:
                destroy(n)

    def play(self):
        self.playing_notes = list()
        self.sounds = list()
        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")

        for note in (self.note_parent.children + self.fake_notes_parent.children):
            # self.play_note(note=int(n.y * 8), delay=int(n.x))
            self.sound.set_play_rate((note.y * 8 * 1.05946309436))

            s = Sequence()
            print('wait:',(note.x * 2))
            s.append(Wait((note.x * 2)))
            s.append(SoundInterval(self.sound))
            self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()

    def stop(self):
        print('stop')
        for s in self.playing_notes:
            s.finish()


    def add_note(self, x=0, y=0, strength=1, length=1/4):
        print('adding note at: ', x, y)
        x *= self.loop_area.scale_x
        n = Note()
        n.length = length
        n.reparent_to(self.note_parent)
        n.position = (round(x * snapsettings.position_snap) / snapsettings.position_snap,
                      round(y * snapsettings.position_snap) / snapsettings.position_snap,
                      -1)
        self.draw_fake_notes()


    def play_note(self, number):
        # todo find closest
        print('play note:', number)
        sound = loader.loadSfx("0DefaultPiano_n48.wav")
        distance = 48 - number
        sound.set_play_rate(pow(1 / 1.05946309436, distance))
        sound.play()

    def draw_fake_notes(self):
        if hasattr(self, 'fake_notes_parent'):
            destroy(self.fake_notes_parent)
        self.fake_notes_parent = Entity(parent=self.note_parent)
        print('loops:', self.scale_x / self.loop_area.scale_x)

        # disable out of bounds notes
        for n in self.notes:
            n.enabled = n.x < self.loop_area.scale_x

        # draw fake notes for loops
        for i in range(1, math.ceil(self.scale_x / self.loop_area.scale_x)):
            for n in [n for n in self.notes if n.x < self.loop_area.scale_x]:
                if n.x + (i * self.loop_area.scale_x) >= self.scale_x:
                    break
                clone = FakeNote()
                clone.strength = n.strength
                clone.length = n.length
                clone.color = color.color(60, .5, .5, 1)
                clone.reparent_to(self.fake_notes_parent)
                clone.x = n.x + (i * self.loop_area.scale_x)
                clone.y = n.y


    @property
    def notes(self):
        return [c for c in self.note_parent.children if c.type == 'Note']

class FakeNote(Note):
    def input(self, key):
        pass
    def update(self, dt):
        pass

class NoteArea(Button):
    def __init__(self, note_section, **kwargs):
        super().__init__(**kwargs)
        self.note_section = note_section
        self.highlight_color = self.color

    def on_click(self):
        if not held_keys[self.note_section.require_key]:
            self.note_section.add_note(mouse.point[0], mouse.point[1])

    def input(self, key):
        if key == self.note_section.require_key:
            # hide self so I can drag note section
            self.z = 2
        elif key == self.note_section.require_key + ' up':
            self.z = 0



class LoopButton(Draggable):
    def __init__(self, note_section):
        super().__init__(
            origin = (.5, -.5),
            position = (1, 0, -.3),
            scale = (1/16, 1),
            color = color.green,
            y_lock = True
            )
        self.note_section = note_section
        self.parent = note_section


    def update(self, dt):
        super().update(dt)
        if self.dragging:
            self.world_x = max(self.world_x, self.note_section.world_x + .25)

    def drop(self):
        print('drop loop buttoin')
        self.world_x = round(self.world_x * 4) / 4
        self.note_section.scale_x *= self.x
        self.scale_x /= self.x
        self.note_section.note_parent.scale_x /= self.x
        self.x = 1
        self.note_section.draw_fake_notes()


count_lines(__file__)

if __name__ == '__main__':
    app = PandaEditor()
    window.color = color.color(0, 0, .12)
    camera.orthographic = True
    camera.fov = 10

    t = NoteSection()
    t.add_note(0, 1/16)
    t.add_note(.25, 2/16)
    t.add_note(.5, 3/16)
    t.add_note(.75, 2/16)
    app.run()
