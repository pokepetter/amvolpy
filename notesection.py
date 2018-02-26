from pandaeditor import *
from direct.interval.IntervalGlobal import Sequence, Func, Wait, SoundInterval

class NoteButton(Button):

    def __init__(self):
        super().__init__()
        self.color = color.dark_gray

        self.on = False

    # def on_mouse_enter()

    def on_click(self):
        print('toggle')
        self.on = not self.on

        if self.on:
            self.color = color.cyan
        else:
            self.color = color.dark_gray

class NoteSection(Entity):

    def __init__(self):
        super().__init__()
        # self.parent = camera.ui
        self.model = 'quad'
        self.origin = (-.5, -.5)
        self.position = (-5, -5)
        self.color = color.color(0, 0, .06)
        self.scale *= 8
        self.collider = 'box'

        self.notes = list()
        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
        # self.position = ()


        # self.play_button = Button()
        # self.play_button.parent = self
        # self.play_button.color = color.pink
        # self.play_button.origin = (-.5, -.5, .01)
        # self.play_button.reparent_to(self)
        # self.play_button.scale_x = 1/8
        # self.play_button.scale_y /= 2
        # self.play_button.y += 1/16
        # self.play_button.x += 1/16


        for y in range(16):
            e = Panel()
            e.parent = self
            e.scale_y = .008
            e.color = color.color(0, 0, .08)
            e.origin = (-.5, 0)
            e.y = y / 16
            e.z = -.01

        for x in range(4):
            e = Panel()
            e.parent = self
            e.scale_x    = .008
            e.color = color.color(0, 0, .08)
            e.origin = (0, -.5)
            e.x = x / 4
            e.z = -.01

        self.notes = list()


    def input(self, key):
        if key == 'space':
            self.play()
        if key == 't':
            self.test()


    def on_click(self):
        self.add_note(mouse.point[0], mouse.point[1])


    def play(self):
        self.playing_notes = list()
        self.sounds = list()

        for n in (self.notes):
            # self.play_note(note=int(n.y * 8), delay=int(n.x))
            sound = loader.loadSfx("0DefaultPiano_n48.wav")
            sound.set_play_rate(1 + (n.y * 8 * .05946309436))

            s = Sequence()
            print('wait:',(n.x * 2))
            s.append(Wait((n.x * 2)))
            s.append(SoundInterval(sound))
            self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()


    def add_note(self, x=0, y=0, strength=1, duration=1/4):
        n = Note()
        n.reparent_to(self)
        n.position = (x, y)
        self.notes.append(n)
        print('added note')


class Note(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.rotation_z = 45
        self.color = color.lime
        self.scale *= .5
        self.z = -.1
        self.collider = 'box'

        self.length_indicator = Entity()
        self.length_indicator.parent = self
        self.length_indicator.model = 'quad'
        self.length_indicator.origin = (-.5, 0)
        self.length_indicator.rotation_z = -45
        self.length_indicator.color = self.color
        self.length_indicator.scale_y = .1
        self.length = 0
        # self.length = 1/8

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value
        self.length_indicator.scale_x = value * 10


    def update(self, dt):
        if mouse.left and self.hovered:
            self.length += dt


if __name__ == '__main__':
    app = PandaEditor()
    window.color = color.color(0, 0, .12)
    # camera.fov = 10
    # cursor = Cursor()
    # cursor.color = color.white33
    camera.orthographic = True

    t = NoteSection()
    app.run()
