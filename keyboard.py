from ursina import *
from note_section import NoteSection

# import rtmidi
import scale_changer
# from note_recorder import NoteRecorder
# import scale_changer, note_recorder

use_midi = False
if use_midi:
    from pygame import midi


class Keyboard(Entity):
    def __init__(self):
        super().__init__(eternal=True)

        self.keys = [char for char in 'zxcvbnmasdfghjklqwertyuio1234567890']
        # printvar(scalechanger.pattern)
        self.octave_offset = 0
        self.note_offset = 0

        self.note_names = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C')

        self.virtual_keyboard = Button(
            parent=camera.ui,
            model='quad',
            origin=(-.5,-.5),
            position=window.bottom_left,
            scale=(1*camera.aspect_ratio, .02),
            color=color.black,
            pressed_scale=1,
            pressed_color=color.black,
            highlight_color=color.black
            )
        self.virtual_keyboard.highlight = Entity(parent=self.virtual_keyboard, model='quad', origin=(-.25,-.5), scale_x=1/79, z=-1, color=color.azure)
        def virtual_keyboard_update():
            self.virtual_keyboard.highlight.enabled = self.virtual_keyboard.hovered
            if self.virtual_keyboard.hovered:
                self.virtual_keyboard.highlight.x = int(mouse.point[0] * 79) / 79

        self.virtual_keyboard.update = virtual_keyboard_update

        self.notes_text = Text(
            text=''.join(self.note_names) * 5,
            font='VeraMono.ttf',
            position=window.bottom_left + Vec2(0,.005),
            origin=(-.5,-.5),
            scale=.5*.75,
            z=-1,
            add_to_scene_entities=True
            )

        def on_click():
            note_to_play = int(mouse.point[0] * 79)
            text = self.notes_text.text.split()[note_to_play]
            note_to_play = (int(text[-1:]) * len(scale_changer.pattern)) + self.note_names.index(text[:-1])
            self.play_note(note_to_play)

        self.virtual_keyboard.on_click = on_click

        self.update_note_names()

        self.parent = camera.ui
        self.scale *= .025
        self.position = (-.5 * camera.aspect_ratio, -.5)

        self.midi_input = None
        if use_midi:
            midi.init()
            if midi.get_default_input_id() != -1:
                self.midi_input = midi.Input(midi.get_default_input_id())
                scale_changer.pattern = (1,)*12

        self.fallback_ns = NoteSection(enabled=False, name='fallback_ns')
        scene.entities.remove(self.fallback_ns)



    def play_note(self, i, velocity=1):
        note_num = i + (self.octave_offset * len(scale_changer.pattern)) + self.note_offset
        original_note = note_num
        note_num = scale_changer.note_offset(note_num)
        note_sections = [e for e in scene.entities if 'NoteSection' in e.types and e.selected and e != self.fallback_ns]

        if not note_sections:
            # print('playing fallback')
            self.fallback_ns.play_note(note_num, velocity, show_overlay=False)
            return

        # print('--', i)
        for ns in note_sections:
            ns.play_note(note_num, velocity, show_overlay=True, original_note=original_note)
            # if i < len(self.children):
            #     self.children[i].color = color.lime

        # print(base.note_recorder.recording)
        if hasattr(base, 'note_recorder') and base.note_recorder.recording:
            base.note_recorder.start_note(i, velocity)


    def stop_note(self, i):
        note_num = i + (self.octave_offset * len(scale_changer.pattern))
        original_note = note_num
        note_num = scale_changer.note_offset(note_num)
        # print('stop note', base.notesheet.prev_selected)
        note_sections = [e for e in scene.entities if 'NoteSection' in e.types and e.selected]
        for ns in note_sections:
            ns.stop_note(note_num, original_note=original_note)
            # print('stopped note')
            if i < len(self.children):
                self.children[i].color = color.unpressed_color

        if not note_sections:
            # print('playing fallback')
            self.fallback_ns.stop_note(note_num)

        if hasattr(base, 'note_recorder') and base.note_recorder.recording:
            base.note_recorder.stop_note(i)




    def input(self, key):
        if held_keys['control']:
            return

        for i, k in enumerate(self.keys):
            if key == k:
                self.play_note(i)

            if key == k + ' up':
                self.stop_note(i)

        if key == ',':
            # print('noteoffset -')
            self.octave_offset -= 1
            self.octave_offset = max(self.octave_offset, 0)

        if key == '.':
            # print('noteoffset +')
            self.octave_offset += 1
            self.octave_offset = min(self.octave_offset, 5)


        if key == '+':
            self.note_offset += 1
        if key == '-':
            self.note_offset -= 1


    def update(self):
        if not self.midi_input:
            # print('no midi device')
            return

        # msg = self.midiin.get_message()
        # print(msg)
        # if msg:
        #     message, deltatime = msg
        #     # print("[%s] @%0.6f %r" % (port_name, timer, message))
        #     print(message)

        # return
        # print(self.player.poll())
        midi_events = self.midi_input.read(10)
        # midi_evs = midi.midis2events(midi_events, self.player.device_id)
        if midi_events:
            # print(midi_events)
            for e in midi_events:
                # print(e[0])
                # 0:?, 1:note, 2:velocity
                # if e[0][0] == 149: # note
                code, note, velocity, unused = e[0]
                if code in (149, 144): # note
                    if velocity > 0:
                        # print('note on:', e[0][1], 'vel:', e[0][2]/128)
                        self.play_note(note, velocity/128)
                    elif velocity <= 0:
                        self.stop_note(note)
                    else:
                        pass
                        # print('note off:', e[0][1])
                elif code == 128:
                    self.stop_note(note)

    # def instantiate_note_overlays(self):
    #     for i in range(128):
    #         nb = Button()
    #         nb.parent = self
    #         nb.scale_y = 1
    #         nb.x = i
    #         nb.text = 'N'
    #         nb.text_entity.y = -.25
    #         nb.origin = (-.5, -.5)


    def update_note_names(self):
        self.notes_text.text = ''
        text = ''
        for i in range(79):
            note_name = self.note_names[scale_changer.note_offset(i, True)] + str(i // len(scale_changer.pattern))[:1]
            text += note_name + (' ' * (4-len(note_name)))

        self.notes_text.text = text
        # for i, child in enumerate(self.children):
        #     if i % len(base.scale_changer.pattern) == 0:
        #         child.color = color.black66 * .8
        #     else:
        #         child.color = color.black66
        #
        #     child.unpressed_color = child.color
        #     child.text = self.note_names[base.scale_changer.note_offset(i, True)] + str(i // len(base.scale_changer.pattern))

if __name__ == '__main__':
    app = Ursina()
    import style
    camera.orthographic = True

sys.modules[__name__] = Keyboard()

camera.fov = 6
if __name__ == '__main__':
    # # base.scale_changer = ScaleChanger()
    # # base.note_recorder = NoteRecorder()
    # t = time.time()
    # base.keyboard = Keyboard()
    # print('----', time.time() - t)

    # ref = Entity(parent=camera.ui, model='quad', scale_x=window.aspect_ratio, texture='amvol_ui_ref', z=-1, color=color.white33)

    app.run()
