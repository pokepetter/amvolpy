from pandaeditor import*
from notesection import NoteSection

app = PandaEditor()

canvas = Panel()
ns = NoteSection()
ns.parent = canvas
ns.scale = ((1 / 10) - .01, (1 / 10) - .01)

app.run()
