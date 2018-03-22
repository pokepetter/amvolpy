from pandaeditor import*
from notesheet import NoteSheet
from notesection import NoteSection

color.notesection = color.color(0, 0, .08)

app = PandaEditor()
camera.orthographic = True
camera.fov = 60
note_sheet = NoteSheet()

ns = NoteSection()


app.run()
