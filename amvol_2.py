from ursina import *

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 1
#
#
# middle_bar = Draggable(parent=scene, model='quad', origin_y=.0, collider='box', color=color._16, scale=(10,.05), z=-10, y=.0, lock=(1,0,1), min_y=-.425, max_y=.5-.025)
# middle_bar.highlight_color = middle_bar.color
# play_button = Button(parent=middle_bar, world_scale=.04, z=-.1, color=color.red, text='>')
# play_button.text_entity.scale = 1
#
# composer = Entity(position=(-.85, 0, 0))
# middle_bar.drag = Func(setattr, composer, 'world_parent', middle_bar)
# middle_bar.drop = Func(setattr, composer, 'world_parent', scene)
# # note_section_size = .05*.8
# composer.bg = Entity(parent=composer, model='quad', color=color._32, origin_y=.5, z=.1, scale=10)
# composer.grid = Entity(parent=composer, model=Grid(8*4,8), origin=(-.5,.5), y=-.05, scale=(.05*.8 *10*4, .05*.8 *10), color=color._84)
#
# class NoteSection(Draggable):
#     def __init__(self, **kwargs):
#         super().__init__(parent=composer, model='quad', origin=(-.5,-.5), step=(.1/4,.1,0), color=color.azure, scale=.05, y=-.1)
#         self.step = (self.scale_x/4, self.scale_y, 0    )
#         self.outline = Entity(parent=self, model=Quad(mode='line', radius=0), origin=self.origin)
#     #     self.drag_bar = Draggable(parent=composer, model='quad', origin=(.5,-.5), z=-.1, step=self.step, color=color.yellow, scale=(.005,self.scale_y))
#         self.notes = []
#     #
#     # def update(self):
#     #     super().update()
#     #     if self.drag_bar.dragging:
#     #         self.scale_x = self.drag_bar.world_x - self.world_x
#     #         self.drag_bar.world_scale_x = .05
#     #     else:
#     #         self.drag_bar.x = self.x + self.scale_x
#     #         self.drag_bar.y = self.y
#
#
# current_note_section = NoteSection()
#
#
# note_editor = Entity(model='quad', color=color.black, origin=(-.5,-.5), x=-.475*window.aspect_ratio, y=-.2 , scale_x=.475*window.aspect_ratio*2, scale_y=.8, collider='box', z=1)
# # note_editor.set_scissor(Vec3(-.5,-.0,0), Vec3(.5,1,0))
#
# current_note = None
# note_editor.target_y = note_editor.y
# h = 7*7
# w = int(.475*window.aspect_ratio*2*64)
#
# # scale_y = scale_x
# grid = Entity(parent=note_editor, model=Grid(w,h), origin=(-.5,-.5), position=(0,0), z=-.01, color=color._32)
# note_names = '\n'.join(('1234567'*7))
# t = Text(parent=note_editor, origin=(.5,.5), font='VeraMono.ttf', text=note_names, z=-1, position=(-.505,1), world_scale=10)
#
# note_editor.add_script(Scrollable(min=-.32, max=.02, scroll_smoothing=8))
# # note_renderer = Entity(parent=note_editor, z=-1, model=Mesh(vertices=[], mode='point', thickness=.5), texture='circle', x=1/w/2, y=1/h/2, color=color.light_gray, scale=(1/w, 1/h, 1), always_on_top=True)
# note_editor.cursor = Entity(model='quad', parent=note_editor, scale=(1/w, 1/h), origin=(-.5,-.5), color=color.azure, z=-.1)
# note_editor.help_line = Entity(model='quad', scale_y=.0025, parent=note_editor, origin_x=-.5, color=color.azure, z=-.2, y=1/7*3)
# Entity(parent=grid, model=Grid(w/16, 7, thickness=2), origin=(-.5,-.5), color=color.dark_gray)
#
# note_parent = Entity(parent=note_editor, scale=(1/w, 1/h), model='quad', color=color.green, origin=(-.5,-.5), z=-.2)
#
# def input(key):
#     global current_note
#
#     if note_editor.hovered and key == 'left mouse down':
#         x = int(mouse.point.x * w)
#         y = int(mouse.point.y * h)
#         # print(x, y)
#         # move note
#         for note in current_note_section.notes:
#             if note.y == y and note.x <= x and note.x+note.scale_x > x:
#                 if held_keys['shift'] and x > note.x+note.scale_x-2:
#                     print('resize note')
#                     current_note = note
#                     return
#
#                 print('drag note')
#                 current_note = None
#                 note.start_dragging()
#                 return
#
#
#         note = Draggable(parent=note_parent, model='quad', x=x, y=y,  origin=(-.5,-.5), color=color.azure, collider=None, step=(1,1,0),
#             texture='horizontal_gradient', texture_scale=(.25,1),
#             )
#         note.drop = Func(setattr, note, 'collision', False)
#         current_note_section.notes.append(note)
#         current_note = note
#
#     if current_note and key == 'left mouse up':
#         current_note = None
#
#
#
#
# def note_editor_update():
#     if current_note and mouse.left and note_editor.hovered:
#         x = int(mouse.point.x * w) + 1
#         current_note.scale_x = x - current_note.x
#         current_note.scale_x = max(current_note.scale_x, 1)
#
# note_editor.update = note_editor_update


#
#     if note_editor.hovered:
#         x = int(mouse.point.x * w)
#         y = int(mouse.point.y * h)
#
#         if key == '1':
#             for i in range(16):
#                 current_note_section.notes.add(Vec3(x+i, y, 1))
#         if key == '2':
#             for i in range(8):
#                 current_note_section.notes.add(Vec3(x+i, y, 1))
#         if key == '4':
#             for i in range(4):
#                 current_note_section.notes.add(Vec3(x+i, y, 1))
#
#         if key == '3':
#             for i in range(6):
#                 current_note_section.notes.add(Vec3(x+i, y, 1))
start_hz = 440
note_index = 69 # A4
twelfth_root_of_two = pow(2, 1/12)

possible_note_frequencies = [440 for i in range(128)]
for i in range(128):
    possible_note_frequencies[i] = start_hz * pow(twelfth_root_of_two, i-69)


# print(possible_note_frequencies)

# for e in possible_note_frequencies
#
# key_map = dict()
# for i, e in enumerate('asdfghjkl'):
#     key_map[e] = 69+i
# for i, e in enumerate('zxcvbnm,.'):
#     key_map[e] = 60+i
#
offset = 60
keyboard_keys = 'zxcvbnm,.asdfghjklqwertyuio123456789'

# def update():
#     for i, key in enumerate(keyboard_keys):
#         if held_keys[key]:
#             # print(possible_note_frequencies[i+offset])
#             diff = (possible_note_frequencies[i+offset] - 440)
#             print(diff)
#             pitch = 1 + (diff / 440)
#
#             play_note(pitch)

def input(key):
    if key in keyboard_keys:
        i = keyboard_keys.index(key)
        press_note(i, length=1)


def press_note(i, volume=1, length=1/4):
    import scale_changer
    scale_changer.pattern = (3,2,2,3,2)
    print(i)
    i = scale_changer.note_offset(i) - 20

    diff = (possible_note_frequencies[i+offset] - 440)
    pitch = 1 + (diff / 440)
    play_note(pitch, length=length, volume=volume)


def play_note(pitch, length=1/8, volume=1):
    a = Audio('0_default_piano_n48', loop=True, pitch=pitch, volume=volume)
    a.fade_out(duration=length)


seqs = []
s = Sequence(loop=True)
for i in range(0,4):
    s.append(Func(press_note, i))
    s.append(Wait(1/8))

seqs.append(s)

s = Sequence(loop=True)
for i in range(2, 7, 2):
    s.append(Func(press_note, i))
    s.append(Wait(1/8))
    print(i)
seqs.append(s)

#
# random.seed(0)
# s = Sequence(loop=True)
# for i in range(12):
#     s.append(Func(press_note, random.randint(5, 14), length=1, volume=.1))
#     s.append(Wait(1/2))
#
# seqs.append(s)




def update():
    for s in seqs:
        s.paused = not held_keys['space']


    # NoteEditor()

if __name__ == '__main__':
    app.run()
