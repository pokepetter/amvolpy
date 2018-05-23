from pandaeditor import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait, SoundInterval
from note import Note
import snapsettings


class NoteSection(Entity):

    def __init__(self):
        super().__init__()

        self.name = 'notesection'
        # self.parent = camera.ui
        # self.model = 'quad'
        # self.origin = (-.5, -.5)
        # self.position = (-5, -5)
        # self.color = color.color(0, 0, .06)
        # self.scale *= 8
        # self.collider = 'box'

        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")

        self.bg = Entity(
            model='quad',
            origin=(-.5, -.5),
            color = color.color(0, 0, .06),
            collider = 'box'
            )

        self.note_parent = Entity(parent=self)

        self.header = Header()
        self.header.parent = self.bg
        self.resize_button = ResizeButton()
        self.resize_button.parent = self.header
        self.resize_button.note_section = self

        #GRID
        self.grid = Grid(4, 16, parent=self, z=-.1, color=color.gray)
        self.grid.color = color.color(0, 0, .12)

        self.notes = list()


    def input(self, key):
        if key == 'space':
            self.play()

    def on_click(self):
        print('click')
        if base.notesheet.mode == 'note':
            self.add_note(mouse.point[0], mouse.point[1])


    def play(self):
        self.playing_notes = list()
        self.sounds = list()

        for note in (self.note_parent.children):
            # self.play_note(note=int(n.y * 8), delay=int(n.x))
            sound = loader.loadSfx("0DefaultPiano_n48.wav")
            sound.set_play_rate((note.y * 8 * 1.05946309436))

            s = Sequence()
            print('wait:',(note.x * 2))
            s.append(Wait((note.x * 2)))
            s.append(SoundInterval(sound))
            self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()


    def input(self, key):
        if key == 'space':
            self.play()

    def add_note(self, x=0, y=0, strength=1, length=1/4):
        print('adding note at: ', x, y)
        n = Note()
        n.length = length
        n.reparent_to(self.note_parent)
        n.position = (round(x * snapsettings.position_snap) / snapsettings.position_snap,
                      round(y * snapsettings.position_snap) / snapsettings.position_snap,
                      -.1)


    def play_note(self, number):
        # todo find closest
        print('play note:', number)
        sound = loader.loadSfx("0DefaultPiano_n48.wav")
        distance = 48 - number
        sound.set_play_rate(pow(1 / 1.05946309436, distance))
        sound.play()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self.color = color.light_gray
        else:
            self.color = color.gray

class Grid(Entity):
    def __init__(self, w, h, **kwargs):
        super().__init__(**kwargs)

        verts = list()
        for x in range(w+1):
            verts.append((x/w, 0, 0))
            verts.append((x/w, 1, 0))
        for y in range(h+1):
            verts.append((0, y/h, 0))
            verts.append((1, y/h, 0))

        self.model = Mesh(verts, mode='line')

        self.background = Entity(parent=self, model='quad')


class Header(Button):

    def __init__(self):
        super().__init__(
            # parent = self.model,
            # model = 'quad',
            color = color.red,
            origin = (-.5, .5),
            # x = .5,
            y = 1,
            z = -.1,
            scale_y = 2 / 16,
            collider = 'box'
            )


class ResizeButton(Draggable):
    def __init__(self):
        super().__init__(
            origin = (.5, .5),
            position = (1, 0, -.1),
            scale = (1/16, 1),
            color = color.green,
            y_lock = True
            )

    def drop(self):
        print('DROP', mouse.delta_drag)
        self.note_section.bg.scale_x *= self.x
        self.x = 1
        self.y = 0
        # self.scale_x = .1 / self.parent.scale_x



if __name__ == '__main__':
    app = PandaEditor()
    window.color = color.color(0, 0, .12)
    # cursor = Cursor()
    # cursor.color = color.white33
    camera.orthographic = True
    camera.fov = 10

    t = NoteSection()
    t.add_note(0, 1/16)
    t.add_note(.25, 2/16)
    t.add_note(.5, 3/16)
    t.add_note(.75, 2/16)
    # g = Grid(20, 20)
    app.run()
