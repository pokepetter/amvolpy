from ursina import *

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 1


middle_bar = Entity(parent=scene, model='quad', origin_y=.0, collider='box', color=color._16, scale=(10,.05), z=-10, y=-.0425, lock=(1,0,1), min_y=-.425, max_y=.5-.025)
middle_bar.highlight_color = middle_bar.color
play_button = Button(parent=middle_bar, world_scale=.04, z=-.1, color=color.red, text='>')
play_button.text_entity.scale = 1
playing = False

composer = Entity(position=(-.85, middle_bar.y, 0))
middle_bar.drag = Func(setattr, composer, 'world_parent', middle_bar)
middle_bar.drop = Func(setattr, composer, 'world_parent', scene)
# note_section_size = .05*.8
composer.bg = Entity(parent=composer, model='quad', color=color._32, origin_y=.5, z=.1, scale=10, collider='box')
composer.grid = Entity(parent=composer, model=Grid(8*4,8), origin=(-.5,.5), y=-.05, scale=(.05*.8 *10*4, .05*.8 *10), color=color._84)

def composer_input(key):
    if key == 'double click' and mouse.hovered_entity == composer.bg:
        print(composer.cursor.position)
        ns = NoteSection(position=composer.cursor.position)
        note_sections.append(ns)


composer.input = composer_input

composer.cursor = Entity(parent=composer, model='wireframe_quad', z=-.1, color=color.cyan, scale=.05, origin=(-.5,-.5))
def composer_update():
    if mouse.hovered_entity == composer.bg:
        composer.cursor.position = mouse.point * 10
        composer.cursor.x = clamp(composer.cursor.x, 0, 10)
        composer.cursor.x = round_to_closest(composer.cursor.x-.025, .05)
        composer.cursor.y = clamp(composer.cursor.y, -8, 0)
        composer.cursor.y = round_to_closest(composer.cursor.y-.025, .05)

composer.update = composer_update

class Resizer(Draggable):
    def __init__(self, note_section):
        super().__init__(parent=note_section, model='quad', world_scale_x=.005, color=color.white, z=-.1, x=1, origin=(.5,-.5), collider='box', alpha=.1, lock=(0,1,1), step=(.025,0,0))
        self.note_section = note_section
    def drag(self):
        self.world_parent = composer
    def drop(self):
        self.note_section.scale_x = self.x - self.note_section.x
        self.world_parent = self.note_section
        self.position = (1,0,-.1)
        self.world_scale_x = .005
        print('------', self.note_section.scale_x)
        self.note_section.texture_scale = (self.note_section.scale_x/.05, 1)



class NoteSection(Draggable):
    def __init__(self, **kwargs):
        super().__init__(parent=composer, model='quad', origin=(-.5,-.5), step=(.1/4,.1,0), texture='white_cube', color=color.azure, scale=.05, y=-.1, alpha=.5)
        self.step = (self.scale_x/4, self.scale_y, 0    )
        self.outline = Entity(parent=self, model=Quad(mode='line', radius=0), origin=self.origin, alpha=.1)
    #     self.drag_bar = Draggable(parent=composer, model='quad', origin=(.5,-.5), z=-.1, step=self.step, color=color.yellow, scale=(.005,self.scale_y))
        self.notes = []
        self.length = 32 # number of 1/4 notes
        self.loops = 1
        self._seq = None
        self.resizer = Resizer(self)


        for key, value in kwargs.items():
            setattr(self, key, value)



    def play(self, start=0):
        print(self)
        if self._seq:
            self._seq.kill()

        self._seq = Sequence(auto_destroy=False, looping=True)
        for n in self.notes:
            self._seq.extend([Wait(n.x/8), Func(play_note, n.y, length=n.scale_x/8)])
        self._seq.start()

    def stop(self):
        if not self._seq:
            return
        self._seq.kill()


note_sections = []
current_note_section = NoteSection()
note_sections.append(current_note_section)


h = 7*7
w = 128
note_names = '\n'.join(('7654321'*7))

def Note(x, y):
    return Draggable(parent=note_editor.note_parent, model='quad', x=x, y=y,  origin=(-.5,-.5), color=color.azure, collider=None, step=(1,1,0), texture='horizontal_gradient', texture_scale=(.25,1))


class NoteEditor(Entity):
    def __init__(self):
        super().__init__(model='quad', color=color.black, origin=(-.5,-.5), x=-.85, y=.005 , scale_x=1/h*w/2, scale_y=.49, collider='box', z=1)

# note_editor = Entity(model='quad', color=color.black, origin=(-.5,-.5), x=-.85, y=.005 , scale_x=1/h*w/2, scale_y=.49, collider='box', z=1)
# note_editor.texture='white_cube'; note_editor.texture_scale=(64,49)

# note_editor.
# note_editor.set_scissor(Vec3(-.5,-.0,0), Vec3(.5,1,0))

        self.current_note = None
        self.target_y = self.y

        self.grid = Entity(parent=self, model=Grid(w,h), origin=(-.5,-.5), position=(0,0), z=-.01, color=color._16)
        Entity(parent=self.grid, model=Grid(w/16, 7, thickness=2), origin=(-.5,-.5), color=color.dark_gray)
        t = Text(parent=self, origin=(.5,.5), font='VeraMono.ttf', text=note_names, z=-1, position=(0,1), world_scale=.4, line_height=1)

        self.add_script(Scrollable(axis='x', scroll_speed=-.1, scroll_smoothing=16))
        self.cursor = Entity(model='quad', parent=self, scale=(1/w, 1/h), origin=(-.5,-.5), color=color.azure, z=-.1)
# note_editor.help_line = Entity(model='quad', scale_y=.0025, parent=note_editor, origin_x=-.5, color=color.azure, z=-.2, y=1/7*3)

        self.note_parent = Entity(parent=self, scale=(1/w, 1/h), model='quad', color=color.green, origin=(-.5,-.5), z=-.2)
        self.limiter = Draggable(parent=self.note_parent, color=color.azure, z=-.1, model=Circle(3), origin=(0,.5), scale=2, step=(1,0,0), lock=(0,1,1), min_x=0, x=64)
        self.limiter.bg = Entity(parent=self.limiter, model='quad', origin=(-.5,-.5), color=color.black66, scale=(128,h))
        self.playing = False

    def get_hovered_note(self):
        x = int(mouse.point.x * w)
        y = int(mouse.point.y * h)

        # move note
        for note in current_note_section.notes:
            if note.y == y and note.x <= x and note.x+note.scale_x > x:
                return note, x, y

        return None, x, y


    def input(self, key):

        if self.hovered and key == 'left mouse down' and not held_keys['shift']:
            # x = int(mouse.point.x * w)
            # y = int(mouse.point.y * h)
            # print(x, y)
            note, x, y = self.get_hovered_note()

            if not note:
                note = Note(x, y)
                note.drop = Func(setattr, note, 'collision', False)
                current_note_section.notes.append(note)
                self.current_note = note

            else:
                # move note
                if held_keys['shift'] and x > note.x+note.scale_x-2:
                    print('resize note')
                    self.current_note = note
                    return

                print('drag note')
                self.current_note = None
                note.start_dragging()
                return


        if self.current_note and key == 'left mouse up':
            self.current_note = None


        if key == 'space':
            self.playing = not self.playing



    def update(self):
        if self.current_note and mouse.left and self.hovered:
            x = int(mouse.point.x * w) + 1
            self.current_note.scale_x = x - self.current_note.x
            self.current_note.scale_x = max(self.current_note.scale_x, 1)


note_editor = NoteEditor()

start_hz = 440
note_index = 69 # A4
twelfth_root_of_two = pow(2, 1/12)

possible_note_frequencies = [440 for i in range(128)]
for i in range(128):
    possible_note_frequencies[i] = start_hz * pow(twelfth_root_of_two, i-69)


# print(possible_note_frequencies)

offset = 60
keyboard_keys = 'zxcvbnm,.asdfghjklqwertyuio123456789'
up_keys = [f'{e} up' for e in keyboard_keys]


class Recorder(Entity):
    def __init__(self):
        super().__init__(recording=False, current_notes=[None for i in range(128)], t=0)

    def input(self, key):
        if held_keys['control'] and key == 'r':
            if not self.recording:
                self.recording = False
                self.t = 0
            else:
                self.t = 0
                self.recording = True

    def update(self):
        if self.recording:
            self.t += time.dt

recorder = Recorder()

class Keyboard(Entity):
    def __init__(self):
        super().__init__()
        self.note_overlays = [Entity(parent=note_editor.note_parent, model='quad', color=rgb(255,255,255,64), origin=(-.5,-.5), z=-.1, scale=(w, 1), y=i, enabled=False) for i in range(h)]


    def input(self, key):
        if key in keyboard_keys:
            y = keyboard_keys.index(key)

            note = Note(0, y)
            # recorder.current_notes[y] = note
            # if recorder.recording:
            #     current_note_section.notes.append(note)
            self.note_overlays[y].enabled = True

        elif key in up_keys:
            y = up_keys.index(key)
            # if recorder.recording and recorder.current_notes[y]:
            #     recorder.current_notes[y].scale_x = current_time - recorder.current_notes[y].x
            # recorder.current_notes[y] = None

            self.note_overlays[y].enabled = False




keyboard = Keyboard()

#         press_note(i, length=1)

def press_note(i, volume=1, length=1/4):
    import scale_changer
    scale_changer.pattern = (3,2,2,3,2)
    print(i)
    i -= held_keys['a'] * 3
    i = scale_changer.note_offset(i) - 10

    diff = (possible_note_frequencies[i+offset] - 440)
    pitch = 1 + (diff / 440)
    play_note(pitch, length=length, volume=volume)


def play_note(pitch, length=1/8, volume=1):
    a = Audio('sine', loop=True, pitch=pitch, volume=volume)
    a.animate('volume', 0, duration=.25, delay=length)
    destroy(a, delay=length+1)



timeline = Entity(parent=composer, model='quad', collider='box', color=color.blue, origin=(-.5,-.5), position=(0,-.05), scale=(2,.05))
def timeline_on_click():
    x = mouse.point.x * timeline.scale_x
    x = round_to_closest(x, .025)
    line.x = x
timeline.on_click = timeline_on_click

line = Draggable(color=color.orange, z=-.1, parent=composer, lock=(False,True,True), scale=.025, y=-.05, origin_y=-.5, min_x=0, max_x=composer.grid.scale_x, step=(.025,0,0))
Entity(parent=line, model=Mesh(vertices=[Vec3(0,0,0), Vec3(0,-1,0)], mode='line', thickness=3), color=color.orange, z=.01, scale_y=2*8)

app.seq = Sequence()
def play(start=0, end=None):
    print('------------', 'play')
    app.seq = Sequence(loop=False, auto_destroy=False)
    for ns in note_sections:
        app.seq.extend([Wait(ns.duration * ns.loops), Func(ns.play)])


def stop():
    [ns.stop() for ns in note_sections]



def input(key):
    if mouse.y > 0 and key == 'space':
        current_note_section.play()


# class Recorder(Entity):
#     def __init__(self):
#         super().__init__()
#         self.recording = False
#
#     def input(self, key):
#         if held_keys['control'] and key == 'r':
#             self.recording = not self.recording
#
#     @property
#     def recording(self):
#         return self._recording
#
#     @recording.setter
#     def recording(self, value):
#         self._recording = value
#         if value:
#             print('start recording')
#         else:
#             print('stop recording')
#
#
# recorder = Recorder()
    # NoteEditor()

if __name__ == '__main__':
    app.run()
