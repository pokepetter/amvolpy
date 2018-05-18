from pandaeditor import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait, SoundInterval
from note import Note
import snapsettings


class NoteSection(Entity):

    def __init__(self):
        super().__init__()

        self.name = 'notesection'
        # self.parent = camera.ui
        self.model = 'quad'
        self.origin = (-.5, -.5)
        # self.position = (-5, -5)
        self.color = color.color(0, 0, .06)
        # self.scale *= 8
        self.collider = 'box'

        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
        self.note_parent = Entity()
        self.note_parent.parent = self
        # self.position = ()

        self.header = Header()
        self.header.parent = self

        # self.play_button = Button()
        # self.play_button.parent = self
        # self.play_button.color = color.pink
        # self.play_button.origin = (-.5, -.5, .01)
        # self.play_button.reparent_to(self)
        # self.play_button.scale_x = 1/8
        # self.play_button.scale_y /= 2
        # self.play_button.y += 1/16
        # self.play_button.x += 1/16

        #GRID

        for y in range(16):
            e = Panel()
            e.parent = self
            e.scale_y = .008
            e.color = color.color(0, 0, .12)
            e.origin = (-.5, 0)
            e.y = y / 16
            e.z = -.01

        for x in range(4):
            e = Panel()
            e.parent = self
            e.scale_x    = .008
            e.color = color.color(0, 0, .12)
            e.origin = (0, -.5)
            e.x = x / 4
            e.z = -.01

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


class Header(Button):

    def __init__(self):
        super().__init__(
            # parent = self.model,
            # model = 'quad',
            color = color.red,
            origin = (-.5, .5),
            x = .5,
            y = 1,
            z = -.1,
            scale_y = 2 / 16,
            collider = 'box'
            )
        self.loop_button = ResizeButton()
        self.loop_button.parent = self

from draggable import Draggable
class ResizeButton(Draggable):
    def __init__(self):
        super().__init__(
        origin = (.5, .5),
        position = (.5, 0, -1),
        scale = (1/16, 1),
        color = color.red
        )
        # self.dragging = False
        # self.add_script(Draggable())

    # def input(self, key):
    #     if key == 'left mouse down' and self.hovered:
    #         self.dragging = True
    #
    #     if key == 'left mouse up' and self.dragging:
    #         print('add', mouse.delta[0])
    #         self.parent.parent.scale_x += mouse.delta[0]
    def drop(self):
        print('DROP')



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
    app.run()
