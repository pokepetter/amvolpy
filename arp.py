from ursina import *



app = Ursina()
import keyboard

camera.orthographic = True
t = time.time()
note_section = NoteSection(size=1, loops=1)
note_section.selected = True
print('----', time.time() - t)
camera.fov = 2

for i, y in enumerate(range(24, 8, -8)):
    note_section.add_note(i/4, y, 1/4, 1)

note_section.draw_notes()

app.run()
