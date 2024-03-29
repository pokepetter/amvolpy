from ursina import *

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 1


window.color = color.black
middle_bar = Entity(parent=scene, model='quad', origin_y=.0, collider='box', color=color._16, scale=(10,.05), z=-10, y=-.0425, lock=(1,0,1), min_y=-.425, max_y=.5-.025)
middle_bar.highlight_color = middle_bar.color

note_sections = []


class Composer(Entity):
    def __init__(self):
        super().__init__(position=(-.85, middle_bar.y, 0))
        self.bg = Entity(parent=self, model='quad', color=color._32, origin_y=.5, z=.1, scale=10, collider='box')
        self.grid = Entity(parent=self, model=Grid(8*4,8), origin=(-.5,.5), y=-.05, scale=(.05*.8 *10*4, .05*.8 *10), color=color._84)
        self.cursor = Entity(parent=self, model='wireframe_quad', z=-.1, color=color.cyan, alpha=.1, scale=.05, origin=(-.5,-.5))
        self.timeline = Entity(parent=self, model='quad', collider='box', color=color.blue, origin=(-.5,-.5), position=(0,-.05), scale=(2,.05))
        self.line = Draggable(color=hsv(210,.8,.5), z=-.1, parent=self, lock=(False,True,True), scale=.025, y=-.05, origin_y=-.5, min_x=0, max_x=self.grid.scale_x, step=(.025,0,0))
        Entity(parent=self.line, model=Mesh(vertices=[Vec3(0,0,0), Vec3(0,-1,0)], mode='line', thickness=3), color=self.line.color, z=.01, scale_y=2*8)

        self.t = 0
        self.playing = False
        self.start_position = 0

        def timeline_on_click():
            x = mouse.point.x * self.timeline.scale_x
            x = round_to_closest(x, .025)
            self.line.x = x
            self.start_position = x
        self.timeline.on_click = timeline_on_click


    def input(self, key):
        if key == 'double click' and mouse.hovered_entity == self.bg:
            print(self.cursor.position)
            ns = NoteSection(position=self.cursor.position)
            note_sections.append(ns)
            print('add note section:', ns.x*20)

        if key == 'space':
            if not held_keys['control'] and not self.line.x == self.start_position:
                self.t = self.start_position
                self.line.x = self.start_position
                self.playing = False
                return

            self.playing = not self.playing


    def update(self):
        if mouse.hovered_entity == composer.bg:
            self.cursor.position = mouse.point * 10
            self.cursor.x = clamp(composer.cursor.x, 0, 10)
            self.cursor.x = round_to_closest(composer.cursor.x-.025, .05)
            self.cursor.y = clamp(composer.cursor.y, -8, 0)
            self.cursor.y = round_to_closest(composer.cursor.y-.025, .05)

            # return
        if not self.playing:
            return

        self.line.x += time.dt / 20
        self.t += time.dt
        # print('----', self.t)

        for ns in note_sections:
            if self.t < (ns.x*20) or self.t > ((ns.x*20) + (ns.scale_x*20)):
                ns.color = color.azure
                continue

            ns.color = color.lime
            ns.t = self.t - (ns.x*20)
            # print(self.t, ns.t)
            ns.line.x = ns.t
            if ns == NoteEditor.current_note_section:
                note_editor.line.x = ns.t * 32

            for note in ns.notes:
                y = int(note.y)
                if not ns.sounds[y].is_playing and ns.t >= note.x/32 and ns.t < (note.x+note.length)/32:
                    ns.start_note(y)
                    print('s:', y)
                    ns.sounds[y].is_playing = True
                elif ns.sounds[y].is_playing and ns.t > (note.x + note.length)/32:
                    ns.stop_note(y)
                    ns.sounds[y].is_playing = False



    def stop(self):
        self.line.x = self.start_position



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


import scale_changer
scale_changer.pattern = (3,2,2,3,2)
scale_changer.scale_rotation = 1

class Note():
    def __init__(self, x, y, length=1, recording=False, **kwargs):
        self.x = x
        self.y = y
        self.length = length
        self.recording = recording


class NoteSection(Draggable):
    def __init__(self, length=32, **kwargs):
        super().__init__(parent=composer, model='quad', origin=(-.5,-.5), step=(.1/4,.1,0), color=color.hsv(random.randint(0, 360), .7, .8), scale=.05, y=-.1, alpha=.5, disabled=True)
        self.step = (self.scale_x/4, self.scale_y, 0    )
        self.outline = Entity(parent=self, model=Quad(mode='line', radius=0), origin=self.origin, alpha=.1)
    #     self.drag_bar = Draggable(parent=composer, model='quad', origin=(.5,-.5), z=-.1, step=self.step, color=color.yellow, scale=(.005,self.scale_y))
        self.notes = []
        self.length = length # number of 1/4 notes
        self.scale_x = .05 * (length/32)
        self.loops = 1
        self._seq = None
        self.resizer = Resizer(self)

        self.samples = [None for i in range(128)]
        self.sounds = [None for i in range(128)]
        self.attack = .1
        self.falloff = 1
        self.loop_samples = False
        # self.instrument = '0_default_piano'
        self.instrument = 'uoiowa_piano'
        self.fadeouts = [None for i in range(128)]

        self.playing = False
        self.recording = False
        # self.current_recording_notes = [None for i in range(128)]

        self.line = Entity(parent=self, model='line', rotation_z=90, scale_x=1, z=-1, color=color.white, origin_x=-.5)
        self.t = 0

        for key, value in kwargs.items():
            setattr(self, key, value)


    def on_click(self):
        NoteEditor.current_note_section = self
        NoteEditor.render()

    # def play(self, start=0):
    #     self.playing = True
        # print(self)
        # if self._seq:
        #     self._seq.kill()
        #
        # self._seq = Sequence(auto_destroy=False, looping=True)
        # for n in self.notes:
        #     self._seq.extend([Wait(n.x/8), Func(play_note, n.y, length=n.scale_x/8)])
        # self._seq.start()

    # def stop(self):
    #     self.playing = False
    #     self.t = 0


    # def update(self):
    #     if not self.playing:
    #         return
    #
    #     self.t += time.dt * 32
    #     self.line.x = self.t / 32
    #     note_editor.line.x = self.t
    #
    #     for note in self.notes:
    #         y = int(note.y)
    #         if not self.sounds[y].is_playing and self.t >= note.x and self.t < note.x+note.scale_x:
    #             self.start_note(y)
    #             print('s:', y)
    #             self.sounds[y].is_playing = True
    #             # print('play')
    #         elif self.sounds[y].is_playing and self.t > note.x + note.scale_x:
    #             self.stop_note(y)
    #             self.sounds[y].is_playing = False


    def start_note(self, i, volume=1):
        original_i = i
        i = scale_changer.note_offset(i) + offset
        if i > 127:
            return
        # print('aaaa', i)
        if self.recording:
            print('record:', composer.t - self.x)
            note = Note(x=(composer.t - self.x)*8, y=original_i, recording=True)
            # self.current_recording_notes[i] = note
            self.notes.append(note)
            note_editor.render()


        if self.fadeouts[i]:
            self.fadeouts[i].kill()
            self.fadeouts[i] = None

        s = Sequence()
        for j in range(int(self.attack*60)+1):
            s.append(Wait(j/60))
            s.append(Func(setattr, self.sounds[i], 'volume', lerp(0, volume, j/int(self.attack*60))))

        self.fadeouts[i] = s
        # if not self.loop_samples:
        self.sounds[i].play()
        s.start()


    def stop_note(self, i):
        original_i = i
        i = scale_changer.note_offset(i) + offset
        if i > 127:
            return
        print('stop note:', i)
        if self.fadeouts[i]:
            self.fadeouts[i].kill()
            self.fadeouts[i] = None

        if self.recording:
            for note in self.notes:
                if note.y == original_i and note.recording:
                    end = (composer.t - self.x) * 8
                    note.length = end - note.x
                    note.recording = False
                    print('stop reccccc', self.t, note.x)

        current_volume = self.sounds[i].volume
        s = Sequence()
        for j in range(int(self.falloff*60)+1):
            s.append(Wait(j/60))
            s.append(Func(setattr, self.sounds[i], 'volume', lerp(self.sounds[i].volume, 0, j/int(self.falloff*60))))
        self.fadeouts[i] = s
        s.start()

        # if self.current_recording_notes[i]:
        #     print('stop note:', i, self.t - self.current_recording_notes[i].x)
        #     self.current_recording_notes[i].scale_x = self.t - self.current_recording_notes[i].x


    @property
    def instrument(self):
        return self._instrument

    @instrument.setter
    def instrument(self, name):
        print('---------------', 'set insturment to:', name)
        self._instrument = name

        import instrument_loader
        self.samples_and_pitches, self.attack, self.falloff, self.loop_samples = instrument_loader.load_instrument(name)
        self.sounds = [Audio(e[0], loop=self.loop_samples, pitch=e[1], volume=0, is_playing=False) for e in self.samples_and_pitches]
        print('---------------', self.sounds)



h = 7*7
w = 1024
note_names = '\n'.join(('7654321'*7))


class DraggableNote(Draggable):
    def __init__(self, **kwargs):
        super().__init__(model='quad', origin=(-.5,-.5), color=color.azure, step=(1,1,0), texture='horizontal_gradient', texture_scale=(.25,1), **kwargs)
        self.disabled = True
        self.resizer = Draggable(parent=self, model='quad', color=color.lime, x=1, origin=[.5,-.5], z=-1, lock=(0,1,1), enabled=False, visible_self=False)
        self.resizer.drop = Func(setattr, self.resizer, 'x', 1)

    def input(self, key):
        super().input(key)
        if key == 'shift':
            self.resizer.enabled = True
        elif key == 'shift up':
            self.resizer.enabled = False

    def update(self):
        super().update()
        if self.resizer.dragging:
            self.scale_x *= self.resizer.x
            self.scale_x = round_to_closest(self.scale_x, 1)


    def drag(self):
        if held_keys['alt']:
            return
        [invoke(setattr, e, 'world_parent', self, delay=1/60) for e in NoteEditor.selection if not e == self]

    def drop(self):
        if not NoteEditor.current_note_section:
            return
        [setattr(e, 'world_parent', NoteEditor.note_parent) for e in NoteEditor.selection if not e == self]
        self.save_notes()

    def save_notes(self):
        NoteEditor.current_note_section.notes = []
        for e in NoteEditor.note_cache:
            if not e.enabled:
                continue

            NoteEditor.current_note_section.notes.append(Note(e.x, e.y, e.scale_x))

        NoteEditor.render()
        print('render')

    # def input(self, key):
    #     super().input(key)
    #     if self.hovered and held_keys['alt'] and key == 'left mouse down':
    #         self.enabled = False
    #         self.save_notes()


class NoteEditor(Entity):
    _instance = None    # assigned on __init__
    note_cache = []
    current_note_section = []
    selection = []
    current_note = None # assigned when you create a new note

    def __init__(self):
        NoteEditor._instance = self
        super().__init__(model='quad', color=color.black, origin=(-.5,-.5), x=-.85, y=-.005 , scale_x=1/h*w/2, scale_y=.49, collider='box', z=1)
        # self.current_note = None
        self.target_y = self.y

        # self.grid = Entity(parent=self, model=Grid(w,h), origin=(-.5,-.5), position=(0,0), z=-.01, color=color._16)
        self.grid = Entity(parent=self, model='quad', texture='white_cube', texture_scale=(w,h), origin=(-.5,-.5), position=(0,0), z=-.01, color=color._16)
        Entity(parent=self.grid, model=Grid(w/32, 1, thickness=2), origin=(-.5,-.5), color=hsv(210,.5,.3))
        Entity(parent=self.grid, model=Grid(w/16, 7, thickness=2), origin=(-.5,-.5), color=color._32)
        t = Text(parent=self, origin=(.5,.5), font='VeraMono.ttf', text=note_names, z=-1, position=(-.0005,1), world_scale=.4, line_height=1, color=color.gray)

        self.add_script(Scrollable(axis='x', scroll_speed=-.1, scroll_smoothing=16))
        # self.cursor = Entity(model='quad', parent=self, scale=(1/w, 1/h), origin=(-.5,-.5), color=color.azure, z=-.1)
# note_editor.help_line = Entity(model='quad', scale_y=.0025, parent=note_editor, origin_x=-.5, color=color.azure, z=-.2, y=1/7*3)

        NoteEditor.note_parent = Entity(parent=self, scale=(1/w, 1/h), origin=(-.5,-.5), z=-.2)
        if not NoteEditor.note_cache:
            NoteEditor.note_cache = [DraggableNote(parent=NoteEditor.note_parent, scale_y=.75, enabled=False) for e in range(128)]

        self.timeline = Entity(parent=NoteEditor.note_parent, model='quad', collider='box', color=color._32, origin=(-.5,-.5), position=(0,h), scale=(w,1))
        def timeline_on_click():
            x = mouse.point.x * w
            print(x)
            # x = round_to_closest(x, 1)
            self.line.x = x
            composer.line.x = NoteEditor.current_note_section.x + (self.line.x/w/5)
            self.line.start_dragging()


        self.timeline.on_click = timeline_on_click
        self.line = Draggable(model='quad', color=hsv(210,.8,.5), z=-.5, parent=NoteEditor.note_parent, lock=(False,True,True), scale=[1,1], y=h, origin_y=-.5, min_x=0, max_x=w, step=(1,0,0))
        Entity(parent=self.line, model=Mesh(vertices=[Vec3(0,0,0), Vec3(0,-1,0)], mode='line', thickness=3), color=self.line.color, z=.01, scale_y=h)

        NoteEditor.limiter = Draggable(parent=NoteEditor.note_parent, color=hsv(210,.8,.5), z=-.1, model=Circle(3), origin=(0,.5), scale=2, step=(1,0,0), lock=(0,1,1), min_x=0, x=32)
        def limiter_drop():
            if not NoteEditor.current_note_section:
                return
            print('set note sections length to:', NoteEditor.limiter.x)
            NoteEditor.current_note_section.length = NoteEditor.limiter.x

        NoteEditor.limiter.drop = limiter_drop
        NoteEditor.limiter.bg = Entity(parent=NoteEditor.limiter, model='quad', origin=(-.5,-.5), color=color.black66, scale=(128,h))
        self.playing = False


    @classmethod
    def render(cls):
        if not NoteEditor.current_note_section:
            print('cant render, please set NoteEditor.current_note_section')
            return
        [e.disable() for e in NoteEditor.note_cache]
        for i, note in enumerate(NoteEditor.current_note_section.notes):
            e = NoteEditor.note_cache[i]
            e.enabled = True
            e.x = note.x
            e.y = note.y
            e.scale_x = note.length
            e.color = color.azure
            if e in NoteEditor.selection:
                e.color = color.lime

        NoteEditor.limiter.x = NoteEditor.current_note_section.length

    def input(self, key):
        if key == 'left mouse down':
            if not mouse.hovered_entity in NoteEditor.note_cache:
                NoteEditor.selection = []

            if self.hovered:
                if not held_keys['shift']:
                    NoteEditor.selection = []
                else:
                    if not self in NoteEditor.selection:
                        NoteEditor.selection.append(self)
                    else:
                        NoteEditor.selection.remove(self)

                NoteEditor.render()

            if held_keys['control'] and self.hovered:
                x, y = [int(e) for e in (mouse.point.xy) * Vec2(w, h)]
                # print('add note:', x, y)
                NoteEditor.current_note_section.notes.append(Note(x, y, 2))
                NoteEditor.render()
                mouse.update()
                if mouse.hovered_entity in NoteEditor.note_cache:
                    NoteEditor.current_note = mouse.hovered_entity
                    NoteEditor.current_note.dragging = False
                # print(mouse.hovered_entity)
            if isinstance(mouse.hovered_entity, DraggableNote) and held_keys['alt']:   # delete note
                # print('remove note at:', mouse.hovered_entity.x, mouse.hovered_entity.y)
                x = mouse.hovered_entity.x
                y = mouse.hovered_entity.y
                for n in NoteEditor.current_note_section.notes:
                    if y == n.y and x >= n.x and x <= n.x + n.length:
                        NoteEditor.current_note_section.notes.remove(n)
                NoteEditor.render()

        if key == 'left mouse up' and NoteEditor.current_note:
            NoteEditor.current_note = None


    def update(self):
        # print(self.hovered, NoteEditor.current_note)
        if NoteEditor.current_note and NoteEditor.current_note.hovered:
            # print((mouse.point.x*w - NoteEditor.current_note.x > 1))
            print('drag')




# start_hz = 440
# note_index = 69 # A4
# twelfth_root_of_two = pow(2, 1/12)
#
# possible_note_frequencies = [440 for i in range(128)]
# for i in range(128):
#     possible_note_frequencies[i] = start_hz * pow(twelfth_root_of_two, i-69)


# print(possible_note_frequencies)

offset = 12
keyboard_keys = 'zxcvbnm,.asdfghjklqwertyuio123456789'
up_keys = [f'{e} up' for e in keyboard_keys]


class Keyboard(Entity):
    def __init__(self):
        super().__init__()
        self.note_overlays = [Entity(parent=NoteEditor.note_parent, model='quad', color=rgb(255,255,255,64), origin=(-.5,-.5), z=-.1, scale=(w, 1), y=i, enabled=False) for i in range(h)]


    def input(self, key):
        if key in keyboard_keys:
            y = keyboard_keys.index(key)
            self.note_overlays[y].enabled = True
            NoteEditor.current_note_section.start_note(y)

        elif key in up_keys:
            y = up_keys.index(key)
            self.note_overlays[y].enabled = False
            NoteEditor.current_note_section.stop_note(y)



class Recorder(Entity):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.recording_note_section = None
        self.record_button = Button(scale=.035, text='rec', color=color.magenta, position=(.05,-.04,-1), on_click=self.toggle_recording)

    def input(self, key):
        if held_keys['control'] and key == 'r':
            self.toggle_recording()

        # if self.recording and key in keyboard_keys:
        #     y = keyboard_keys.index(key)
        #     print(int(composer.line.x * 128))
        #     note = Note(int(composer.line.x * 128), y)

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording_note_section = NoteSection(length=32*32)
        self.recording_note_section.recording = True
        NoteEditor.current_note_section = self.recording_note_section
        NoteEditor.render()
        composer.playing = True


    def stop_recording(self):
        if self.recording_note_section:
            self.recording_note_section.recording = False
            self.recording_note_section = None
        NoteEditor.current_note_section = None
        NoteEditor.render()
        composer.playing = False



composer = Composer()
note_editor = NoteEditor()
NoteEditor.current_note_section = NoteSection()
NoteEditor.render()
note_sections.append(note_editor.current_note_section)

keyboard = Keyboard()
play_button = Button(scale=.045, y=-.045, z=-.1, color=color.orange, text='play\nall')
# play_button.world_parent = middle_bar
# play_button.text_entity.scale = 1
# playing = False


middle_bar.drag = Func(setattr, composer, 'world_parent', middle_bar)
middle_bar.drop = Func(setattr, composer, 'world_parent', scene)
recorder = Recorder()

def toggle_play():
    if not NoteEditor.current_note_section.playing:
        NoteEditor.current_note_section.play()
    else:
        NoteEditor.current_note_section.stop()

play_current_note_section_button = Button(text='play\nsolo', position=(-.05,-.04,-1), color=color.azure, scale=.035, on_click=toggle_play)
# def _input(key):
#     if key == 'space':
#         toggle_play()

# play_current_note_section_button.input = _input

def go_to_start():
    composer.t = 0
#
# go_to_start_button = Button(text='|<-', position=(-.1,-.04,-1), color=color.yellow, scale=.03, on_click=go_to_start)


if __name__ == '__main__':
    NoteEditor.current_note_section.notes.extend([Note(0,16,length=4), Note(4,17,length=4), Note(8,18,length=4), Note(12,19,length=4)])
    for e in NoteEditor.current_note_section.notes:
        e.scale_x = 4

    # NoteEditor.current_note_section = current_note_section
    NoteEditor.render()
    app.run()
