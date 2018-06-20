from ursina import *


class LoopButton(Draggable):
    def __init__(self, note_section):
        super().__init__(
            origin = (.5, -.5),
            position = (1, 0, -.3),
            scale = (1/16, 1),
            color = color.green,
            y_lock = True
            )
        self.note_section = note_section
        self.parent = note_section


    def update(self, dt):
        super().update(dt)
        if self.dragging:
            self.world_x = max(self.world_x, self.note_section.world_x + .25)

    def drag(self):
        self.note_section.end_button.reparent_to(self.note_section.parent)

    def drop(self):
        play_button_world_scale_x = self.note_section.play_button.world_scale_x
        end_button_world_scale_x = self.note_section.end_button.world_scale_x

        print('drop loop button')
        self.world_x = round(self.world_x * 4) / 4
        self.note_section.scale_x *= self.x
        self.scale_x /= self.x
        self.note_section.note_parent.scale_x /= self.x
        self.x = 1
        self.note_section.draw_fake_notes()
        self.note_section.end_button.reparent_to(self.note_section)

        self.note_section.play_button.world_scale_x = play_button_world_scale_x
        self.note_section.end_button.world_scale_x = end_button_world_scale_x
