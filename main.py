from ursina import *
import scalechanger
from keyboard import Keyboard
from note_section import NoteSection
# from rec import Rec

app = Ursina()
# color.notesection = color.color(0, 0, .08)
camera.orthographic = True
camera.fov = 4
window.color = color.dark_gray
#
keyboard = Keyboard()
NoteSection()
# # app.rec = Rec()

def input(key):
    if key == 'scroll down':
        camera.fov += .5
    if key == 'scroll up':
        camera.fov -= .5

    if key == 'arrow left':
        note_sections = [e for e in scene.entities if isinstance(e, NoteSection)]
        # [e.world_parent = scaler for e in scene.entities if isinstance(e, NoteSection)]
        # for ns in note_sections:
        #     ns.world_parent = scaler
        scene.scale_x *= .5
        # for ns in note_sections:
        #     ns.world_parent = scene
    # [e.world_parent = scene for e in scene.entities if isinstance(e, NoteSection)]



bar = Entity(parent=camera.ui, model='quad', origin_y=-.5, y=-.5, scale=(camera.aspect_ratio, .1), color=color.brown)

HotReloader(path =__file__)

app.run()
