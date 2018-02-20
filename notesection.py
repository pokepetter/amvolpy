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

        self.model = 'quad'
        self.origin = (-.5, -.5)
        self.position = (-5, -5)
        self.color = color.white33
        self.scale *= 10

        self.notes = list()
        self.sound = loader.loadSfx("0DefaultPiano_n48.wav")
        # self.position = ()

        for y in range(8):
            for x in range(8):
                note_spot = NoteButton()
                note_spot.parent = self

                note_spot.origin = (-.5, -.5)
                note_spot.position = (x/8, y/8, -.01)
                note_spot.scale *= 1/8.2
                self.notes.append(note_spot)

    def input(self, key):
        if key == 'space':
            self.play()
        if key == 't':
            self.test()

    def play(self):
        self.playing_notes = list()
        self.sounds = list()

        for n in (self.notes):
            if n.on:

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


    # def test(self):
    #     self.sound0 = loader.loadSfx("0DefaultPiano_n48.wav")
    #     self.sound1 = loader.loadSfx("0DefaultPiano_n48.wav")
    #     self.sound1.set_play_rate(.5)
    #
    #     s = Sequence()
    #     s.append(SoundInterval(self.sound0))
    #     s.append(Wait(.5))
    #     s.append(SoundInterval(self.sound1))
    #     s.start()
        #
        # self

        # self.scale = (4, 1)
if __name__ == '__main__':
    app = PandaEditor()
    window.color = color.dark_gray
    # camera.fov = 10
    camera.orthographic = True
    t = NoteSection()
    app.run()
