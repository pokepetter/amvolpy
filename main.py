from pandaeditor import *
from keyboard import Keyboard
from notesheet import NoteSheet
from notesection import NoteSection

color.notesection = color.color(0, 0, .08)
if __name__ == '__main__':
    window.position = (0, 0)
    # window.size = (1920, 800)
    app = PandaEditor()
    camera.orthographic = True
    camera.fov = 15
    window.color = color.gray


    app.notesheet = NoteSheet()
    app.keyboard = Keyboard()
    app.mode = 'move'

    # ns = NoteSection()


    app.run()
