from ursina import *


class PlayButton(Button):
    def __init__(self, note_section):
        super().__init__(
            parent = note_section,
            # model = Circle(),
            color = color.yellow,
            position = (0, 1),
            text = '>',
            z = -1.5
            )
        # printvar(Circle())
        # self.model = None
        self.model = Circle(5)
        self.note_section = note_section
        self.text_entity.scale *= 3
        self.scale *= .1


    def on_click(self):
        if not self.note_section.playing:
            base.rec.indicator.world_x = self.world_x
            self.note_section.play()
            # print('play note section click')
        else:
            self.note_section.stop()
