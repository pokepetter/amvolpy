from ursina import *


class EndButton(Draggable):
    def __init__(self, note_section):
        super().__init__(
            parent = note_section,
            origin = (.5, .5),
            position = (1, 1, -.5),
            scale = (1/16, .2),
            color = color.red,
            y_lock = True
            )
        self.note_section = note_section
        # self.parent = note_section
        # self.position = (1, 1, -.4)
        # self.x = 1
        # self.reparent_to(note_section.parent)


    def update(self, dt):
        super().update(dt)
        if self.dragging:
            self.world_x = max(self.world_x, self.note_section.world_x + .25)

    def drop(self):
        # super().drop()
        self.world_x = round(self.world_x * 4) / 4
        print('drop end button')
        self.note_section.note_area.scale_x = self.world_x - self.note_section.world_x

        if self.world_x > self.note_section.world_x + self.note_section.scale_x:
            self.note_section.loop_button_end.world_x = self.world_x
            self.note_section.loop_button_end.drop()
            self.x = 1


        self.note_section.draw_fake_notes()
        destroy(self.note_section.grid)
        print('new grid size: ', int(4 * self.note_section.note_area.scale_x))
        self.note_section.grid = Grid(
            int(4 * self.note_section.note_area.scale_x),
            16,
            parent = self.note_section.note_area,
            z = -.2,
            color = color.tint(self.note_section.color, .3)
            )


if __name__ == '__main__':
    app = Ursina()
    window.color = color.color(0, 0, .12)
    camera.orthographic = True
    camera.fov = 10
    from notesection import *
    t = NoteSection()
    t.add_note(0, 1/16)
    t.add_note(.25, 2/16)
    t.add_note(.5, 3/16)
    t.add_note(.75, 2/16)
    app.run()
