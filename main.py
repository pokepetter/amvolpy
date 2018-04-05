from pandaeditor import *
from keyboard import Keyboard
from notesheet import NoteSheet
from notesection import NoteSection

color.notesection = color.color(0, 0, .08)
if __name__ == '__main__':
    app = PandaEditor()
    camera.orthographic = True
    camera.fov = 10


    app.notesheet = NoteSheet()
    app.keyboard = Keyboard()

    # ns = NoteSection()


    app.run()
