from ursina import *


class EndButton(Draggable):
    def __init__(self, note_section, **kwargs):
        super().__init__(
            model=Circle(),
            parent=note_section,
            lock_y=True,
            position=(1,1,-2),
            color=color.orange,
            step=1/16,
            **kwargs
            )
        self.indicator = Entity(parent=self, z=-.1, model=Mesh(vertices=((0,0,0),(0,-20,0)), mode='line', thickness=2), color=color.white)
        self.note_section = note_section

    def drag(self):
        # self.indicator.enabled = True
        self.step = 1/16 / self.note_section.scale_x


    def drop(self):
        # self.indicator.enabled = False
        self.note_section.loop_button.world_parent = scene
        self.note_section.scale_x = self.x * self.note_section.scale_x
        self.note_section.scale_x = max(self.note_section.scale_x, .05)
        self.note_section.scale_x = int(self.note_section.scale_x * 16) / 16
        self.x = 1
        self.note_section.loop_button.world_parent = self.note_section
        self.z = -2

        if self.x > self.note_section.loop_button.x:
            self.note_section.loop_button.x = self.x
            self.note_section.draw_notes()
        self.note_section.loop_button.drop()


if __name__ == '__main__':
    app = Ursina()
    from note_section import NoteSection
    ns = NoteSection()
    EndButton(ns)
    app.run()
