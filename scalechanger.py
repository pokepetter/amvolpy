from ursina import *


class ScaleChanger():
    def __init__(self):
        self.base_note_offset = 0
        self.scale_rotation = 0

        self.final_offsets = list()
        self.note_scale = (2, 2, 1, 2, 2, 3)
        # self.scale = (1,)*12
        # self.scale = (2,1,2,2,2,1,2)


    @property
    def note_scale(self):
        return self._note_scale

    @note_scale.setter
    def note_scale(self, value):
        self._note_scale = value[self.scale_rotation:]+value[:self.scale_rotation] #rotate scale

        self.final_offsets = list()
        cumulative = 0

        for e in self._note_scale:
            cumulative += e
            self.final_offsets.append(cumulative)


    @property
    def base_note_offset(self):
        return self._base_note_offset

    @base_note_offset.setter
    def base_note_offset(self, value):
        self._base_note_offset = value

    @property
    def scale_rotation(self):
        return self._scale_rotation

    @scale_rotation.setter
    def scale_rotation(self, value):
        self._scale_rotation = value


    def note_offset(self, y, normalize_within_octave=False):
        if y == 0:
            print("no note on 0")
            return 0

        sL = (y-1) / (len(self.note_scale))
        filled_octaves = int(sL)
        offset = self.final_offsets[y - (filled_octaves * (len(self.note_scale))) - 1]

        if normalize_within_octave:
            if offset + self.base_note_offset > 12:
                return (offset + self.base_note_offset) - 12

            return offset + self.base_note_offset

        # print("y:", y)
        return filled_octaves * 12 + offset + self.base_note_offset


    # def input(self, key):
    #     if key.isdigit():
    #         if held_keys['shift']:
    #             self.base_note_offset = int(key)
    #             print('base note offset:', self.base_note_offset)
    #
    #         if held_keys['alt']:
    #             self.scale_rotation = int(key)
    #             printvar('scale_rotation:', self.scale_rotation)
    #
    #     if key == 's':
    #         self.keyboard_graphic.enabled = not self.keyboard_graphic.enabled
    #
    #
    # def on_click(self):
    #     self.menu.enabled = not self.menu.enabled
    #     self.keyboard_graphic.enabled = not self.keyboard_graphic.enabled





sys.modules['scalechanger'] = ScaleChanger()

# Text.size *= .75
# Text.default_font = 'VeraMono.ttf'


class ScaleChangerMenu(Button):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            color=color.orange,
            # scale = .05,
            scale = Text.size * 2,
            text = '|||||',
            y = -.45
            )

        spacing = 2 / 2
        self.keyboard_graphic = Entity(parent=self, scale=.5, position=(spacing, 2.75))
        # self.menu = Button(parent=self, model=Quad(scale=(5,3)), y=2.1, collider=False)
        # self.pattern_slider = Slider(parent=self.menu, scale=8, label='pattern')
        slider = Slider(parent=self, scale=20, vertical=True, max=12, step=1, y=1)
        print(slider.step)

        patterns = (
            (2, 2, 1, 2, 2, 3),
            (1,1,1,1,1,1,1,1,1,1,1,1),
            (2,1,2,2,2,1,2),
            )
        self.button_group = ButtonGroup(
            parent=self,
            options=[str(e).replace(',', '')[1:-1] for e in patterns],
            # title='Scale Pattern',
            scale=1,
            # position=(-self.menu.scale_x*2.5, self.menu.scale_y*1.5)
            )
        # grid_layout(self.button_group.buttons, max_x=1, direction=(1,1,0))
        for i, e in enumerate(self.button_group.buttons):
            e.x = -e.scale_x - spacing
            e.y = (i * e.scale_y) + 1.25
            e.origin_x = -.5
            e.text_entity.origin = (-.55, 0)

        self.visualize_scale()
        # for b in button_group.button:
        # ButtonGroup(('test', 'yolo', 'butt'))
    #     self.menu.on_enable = self.menu_enable
    #
    # def menu_enable(self):
    #     self.menu.scale = 0
    #     self.menu.color = color.clear
    #     self.menu.animate_scale(Vec3(1,1,1), duration=.1, curve=curve.linear)
    #     self.menu.animate_color(Button.color, duration=.1)

    def visualize_scale(self):
        [destroy(c) for c in self.keyboard_graphic.children]
        note_names = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
        new_x = 0
        for i in range(12):
            e = Button(parent=self.keyboard_graphic, origin=(0,.5), scale=(1,4), color=color.white, texture='white_cube')
            new_x += .5
            if i in (1,3,6,8,10):
                e.z = -.1
                e.scale_x *= .7
                e.scale_y *= .6
                e.color = color.dark_gray

            if i == 5 or i == 12:
                new_x += .5

            e.x = new_x
            # e.text = note_names[i]
            # e.text_entity.world_scale = 20

            if (i-scalechanger.base_note_offset in scalechanger.final_offsets
            or i+12-scalechanger.base_note_offset in scalechanger.final_offsets):
                e.color = lerp(e.color, color.cyan, .5)


if __name__ == '__main__':
    app = Ursina()
    ScaleChanger()
    # import scalechanger
    # ScaleChangerMenu()
    app.run()
    # import scalechanger
#     print(1, scalechanger.note_offset(1))
#     print(5, scalechanger.note_offset(5))
#     print(9, scalechanger.note_offset(9))
