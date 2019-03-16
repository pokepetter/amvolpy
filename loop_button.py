from ursina import *


class LoopButton(Draggable):
    def __init__(self, note_section):
        super().__init__(
            model='quad',
            parent=note_section,
            lock_y=True,
            scale=(.05, 1),
            origin_y=.5,
            position=(1,1,-.2),
            color=color.green,
            # min_x=1/16,
            step=1/16
            )
        self.note_section = note_section


    def drop(self):
        self.note_section.end_button.world_parent = scene
        self.note_section.scale_x = self.x * self.note_section.scale_x
        self.note_section.scale_x = max(self.note_section.scale_x, .05)
        self.note_section.scale_x = int(self.note_section.scale_x * 16) / 16
        self.x = 1
        self.note_section.end_button.world_scale_x = .05
        self.note_section.loop_button.world_scale_x = .05
        self.note_section.end_button.world_parent = self.note_section

        self.note_section.draw_notes()
