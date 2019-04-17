from ursina import *
from note_section import NoteSection
from pygame import midi
import scalechanger


class Keyboard(Entity):
    def __init__(self):
        super().__init__()
        self.keys = [char for char in 'zxcvbnmasdfghjklqwertyuiop1234567890']
        printvar(scalechanger.note_scale)
        self.octave_offset = 0

        self.note_names = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
        # self.instantiate_note_overlays()
        # self.update_note_names()
        self.parent = camera.ui
        self.scale *= .025
        self.position = (-.5 * camera.aspect_ratio, -.5)

        midi.init()
        self.player = None
        self.fallback_ns = NoteSection(enabled=False)

        try:
            self.player = midi.Input(midi.get_default_input_id())
            print('found connected midi controller:', self.player)
        except:
            print('no midi controller found')

    def play_note(self, i, velocity=1):
        note_num = i + (self.octave_offset * len(scalechanger.note_scale))
        note_num = scalechanger.note_offset(note_num)
        note_sections = [e for e in scene.entities if 'NoteSection' in e.types and e.selected and e != self.fallback_ns]

        if not note_sections:
            self.fallback_ns.play_note(note_num, velocity, show_overlay=False)
            return

        for ns in note_sections:
            ns.play_note(note_num, velocity, show_overlay=True)
            if i < len(self.children):
                self.children[i].color = color.lime


    def stop_note(self, i):
        # print('yolo')
        note_num = i + (self.octave_offset * len(scalechanger.note_scale))
        note_num = scalechanger.note_offset(note_num)
        # print('stop note', base.notesheet.prev_selected)
        note_sections = [e for e in scene.entities if 'NoteSection' in e.types and e.selected]
        for ns in note_sections:
            ns.stop_note(note_num)
            # print('played note')
            if i < len(self.children):
                self.children[i].color = color.unpressed_color



    def input(self, key):
        if held_keys['control']:
            return

        for i, k in enumerate(self.keys):
            if key == k:
                self.play_note(i)

            if key == k + ' up':
                self.stop_note(i)

        if key == ',':
            print('noteoffset -')
            self.octave_offset -= 1
            self.octave_offset = max(self.octave_offset, -2)

        if key == '.':
            print('noteoffset +')
            self.octave_offset += 1
            self.octave_offset = min(self.octave_offset, 5)


    def update(self):
        if not self.player:
            try:
                self.player = midi.Input(midi.get_default_input_id())
                # print('found connected midi controller:', self.player)
            except:
                pass

            return

        midi_events = self.player.read(10)
        midi_evs = midi.midis2events(midi_events, self.player.device_id)
        # print(midi_events)
        try:
            if midi_events:
                # print(midi_events)
                for e in midi_events:
                    # print(e[0])
                    # 0:?, 1:note, 2:velocity
                    # if e[0][0] == 149: # note
                    if e[0][0] == 144: # note
                        if e[0][2] > 0:
                            # print('note on:', e[0][1], 'vel:', e[0][2])
                            self.play_note(e[0][1], velocity=e[0][2]/128)
                        else:
                            pass
                            # print('note off:', e[0][1])
        except:
            pass

    def instantiate_note_overlays(self):
        for i in range(128):
            nb = Button()
            nb.parent = self
            nb.scale_y = 1
            nb.x = i
            nb.text = 'N'
            nb.text_entity.y = -.25
            nb.origin = (-.5, -.5)


    def update_note_names(self):
        for i, child in enumerate(self.children):
            if i % len(scalechanger.note_scale) == 0:
                child.color = color.black66 * .8
            else:
                child.color = color.black66

            child.unpressed_color = child.color
            child.text = self.note_names[scalechanger.note_offset(i, True)] + str(i // len(scalechanger.note_scale))



if __name__ == '__main__':
    app = Ursina()
    keyboard = Keyboard()
    app.run()
