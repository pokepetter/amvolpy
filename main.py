from pandaeditor import *
from keyboard import Keyboard
from notesheet import NoteSheet
from notesection import NoteSection

color.notesection = color.color(0, 0, .08)


    # ns = NoteSection()
class Amvol(Entity):

    def __init__(self):
        super().__init__()
        # window.position = (0, 0)
        # window.size = (1920, 800)
        camera.orthographic = True
        camera.fov = 15
        window.color = color.gray

        app.notesheet = NoteSheet()
        app.keyboard = Keyboard()

    #     app.mode = 'move'
    #     self.mode_buttons = [c for c in 'qwerty']
    #     self.modes = (
    #         'move',
    #         'write',
    #
    #     )
    #
    # def input(self, key):
    #     if key in self.mode_buttons:
    #         print(self.mode_buttons.index(key))

app = PandaEditor()
amvol = Amvol()
app.run()
