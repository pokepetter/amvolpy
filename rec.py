from pandaeditor import *

class Rec(Entity):
    def __init__(self):
        super().__init__()

        self.parent = base.notesheet
        self.notesection = None
        self.recording = False
        self.indicator = Entity(
            parent = self,
            world_scale_x = .025,
            origin = (0, -.5),
            z = -1,
            model = Mesh(verts=((0,0,0), (0,1,0)), mode='lines'),
            color = color.cyan,
            )


    def stop_recording(self):
        self.notesection = None
        self.recording = False


    def record(self):
        # get tempo before recotding
        # find open space
        self.notesection = base.notesheet.create_note_section(0,0)
        # self.notesection.end_button.x = 100
        # self.notesection.end_button.drop()
        self.recording = True


    def update(self, dt):
        if self.recording:
            pass



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
                    self.notesection.add_note(
                        x = self.indicator.x + self.notesection.x,
                        y = i,
                        strength = 1,
                        length = 0
                        )
                if key == k + ' up':
                    print('stop:', i)
                    fresh_notes = [n for n in self.notesection.notes if n.length == 0]
                    fresh_notes = [n for n in fresh_notes if n.y == i]
                    fresh_notes[0].length = (self.indicator.x + self.notesection.x) - fresh_notes[0].x
                    # stop note with y==i
