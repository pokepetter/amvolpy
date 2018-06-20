from ursina import *
from keyboard import Keyboard
from notesheet import NoteSheet
from notesection import NoteSection
from rec import Rec

color.notesection = color.color(0, 0, .08)


    # ns = NoteSection()
class Amvol(Entity):

    def __init__(self):
        super().__init__()
        camera.orthographic = True
        camera.fov = 15
        window.color = color.gray

        app.notesheet = NoteSheet()
        # app.notesheet.create_note_section(0, 0)
        app.keyboard = Keyboard()
        app.rec = Rec()
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

app = Ursina()
amvol = Amvol()
app.run()
