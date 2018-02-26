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

        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
        self.note_parent = Entity()
        self.note_parent.parent = self
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
        if key == 't':
            self.test()


    def on_click(self):
        self.add_note(mouse.point[0], mouse.point[1])


    def play(self):
        self.playing_notes = list()
        self.sounds = list()

        for note in (self.note_parent.children):
            # self.play_note(note=int(n.y * 8), delay=int(n.x))
            sound = loader.loadSfx("0DefaultPiano_n48.wav")
            sound.set_play_rate(1 + (note.y * 8 * .05946309436))

            s = Sequence()
            print('wait:',(note.x * 2))
            s.append(Wait((note.x * 2)))
            s.append(SoundInterval(sound))
            self.playing_notes.append(s)

        for s in self.playing_notes:
            s.start()


    def add_note(self, x=0, y=0, strength=1, duration=1/4):
        n = Note()
        n.reparent_to(self.note_parent)
        n.position = (round(x * 16) / 16, round(y * 16) / 16)
        print('added note')


class Note(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.rotation_z = 45
        # self.color = color.clear
        self.scale *= .5
        self.z = -.1
        self.collider = 'box'
        self.model = None

        self.length_indicator = Entity()
        self.length_indicator.parent = self
        self.length_indicator.model = 'quad'
        self.length_indicator.origin = (-.5, 0)
        self.length_indicator.rotation_z = -45
        self.length_indicator.color = self.color
        self.length_indicator.scale_y = .2
        self.length = 0

        self.circle = Quad()
        self.circle.parent = self
        self.circle.color = color.lime
        self.circle.z = -.1
        self.max_circle_size = self.circle.scale
        self.strength = .6
        self.press_time = 0

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        value = max(0, value)
        self._length = value
        self.length_indicator.scale_x = value * 10

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = clamp(value, .2, 1)
        self.circle.scale = Point3(1,1,1) * (self._strength + .2)


    def update(self, dt):
        self.press_time += dt
        if self.press_time >= 1/16:
            if mouse.left and self.hovered:
                self.length += 1/16
            if mouse.right and self.hovered:
                self.length -= 1/16

            self.press_time = 0


    def input(self, key):
        if self.hovered:
            if key == 'scroll up':
                self.strength += .2
            elif key == 'scroll down':
                self.strength -= .2




if __name__ == '__main__':
    app = PandaEditor()
    window.color = color.color(0, 0, .12)
    # camera.fov = 10
    # cursor = Cursor()
    # cursor.color = color.white33
    camera.orthographic = True

    t = NoteSection()
    app.run()
