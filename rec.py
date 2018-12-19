from ursina import *

class Rec(Entity):
    def __init__(self):
        super().__init__()

        self.parent = base.notesheet
        self.notesection = None
        self.rec_note_sections = list()
        self.recording = False
        self.indicator = Entity(
            parent = self,
            origin = (0, -.5),
            z = -1,
            model = Mesh(vertices=((0,0,0), (0,1,0)), mode='lines'),
            color = color.cyan,
            )
        self.indicator_start_x = 0


    def stop_recording(self):
        self.notesection = None
        self.recording = False
        for i, ns in enumerate(self.rec_note_sections):
            ns.loop_button_end.world_x = self.indicator.world_x
            ns.loop_button_end.drop()
            ns.end_button.world_x = self.indicator.world_x
            ns.end_button.drop()

            if not ns.notes:
                destroy(ns)

        self.indicator.x = self.indicator_start_x


    def record(self):
        # get tempo before recotding
        # find open space
        self.rec_note_sections = list()
        self.indicator_start_x = self.indicator.x

        self.note_section = base.notesheet.create_note_section(0,0/64)
        self.note_section.end_button.x = 100
        # self.notesection.octave = 0
        invoke(self.note_section.end_button.drop, delay=.001) # have to add delay or panda3d will crash for some reason :S
        self.rec_note_sections.append(self.note_section)
        # for i in range(4):
        #     self.notesection = base.notesheet.create_note_section(0,i/64)
        #     self.notesection.octave = i
        #     self.notesection.end_button.x = 100
        #     invoke(self.notesection.end_button.drop, delay=.001) # have to add delay or panda3d will crash for some reason :S
        #     self.rec_note_sections.append(self.notesection)
        self.recording = True


    def update(self):
        if self.recording:
            self.indicator.world_x += time.dt


    def input(self, key):
        if held_keys['control'] and key == 'r':
            if not self.recording:
                self.record()
            else:
                self.stop_recording()

        # recording, start note
        if not held_keys['control'] and self.recording:
            for i, k in enumerate(base.keyboard.keys):
                if key == k:
                    note_num = i + (base.keyboard.octave_offset * len(base.scalechanger.scale))
                    note_num = base.scalechanger.note_offset(note_num)

                    octave = (note_num // 32)
                    print('pressed:', i, 'add note to octave:', octave, 'at postition:', i-(octave*16))
                    i = i - (octave * 16)
                    printvar(i)
                    # note = self.rec_note_sections[octave].add_note(
                    note = self.note_section.add_note(
                        x = 0,  # set world_x later
                        y = i / 16,
                        strength = 1,
                        length = 0
                        )
                    note.world_x = self.indicator.world_x

                if key == k + ' up':
                    print('stop:', i)
                    # note_num = i + (base.keyboard.octave_offset * len(base.scalechanger.scale))
                    # note_num = base.scalechanger.note_offset(note_num)
                    octave = i//16
                    # ns = self.rec_note_sections[octave]
                    ns = self.note_section
                    fresh_notes = [n for n in ns.notes if n.length == 0]
                    # print('||||||||', i, [int(n.y * 16) for n in fresh_notes])
                    fresh_notes = [n for n in fresh_notes if int(n.y * 16) == i-(16 * octave)]
                    # print('------------', len(fresh_notes))
                    if fresh_notes:
                        fresh_notes[0].length = self.indicator.world_x - fresh_notes[0].x
                #     stop note with y==i
