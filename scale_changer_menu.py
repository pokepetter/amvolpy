from ursina import *
import scale_changer

Button.default_model = 'quad'


class ScaleChangerMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent = camera.ui,
            position=(.4,-.4, -2),
            color=color.orange,
            )

        for key, value in kwargs.items():
            setattr(self, key ,value)



        self.toggle_button = Button(text='scle\ncngr', model='quad', scale=.05, position=(.5,-.45, -2))

        def toggle_enabled():
            if not self.children:
                t = time.time()
                self.create()
                print('creation time:', time.time() - t)
                return

            for c in self.children:
                c.enabled = not c.enabled
        self.toggle_button.on_click = toggle_enabled


    def create(self):
        self.button_group = ButtonGroup(
            parent = self,
            # options = [str(e).replace(',', '')[1:-1] for e in self.patterns],
            options = scale_changer.patterns.keys(),
            )

        for i, e in enumerate(self.button_group.buttons):
            e.origin_x = 0
            e.x = 0
            e.y = i
            e.origin_y = -.5
            e.pattern = scale_changer.patterns[e.text_entity.text]


        self.keyboard_graphic = Entity(parent=self, scale=.025)
        self.keyboard_graphic.x = (self.button_group.buttons[0].scale_x * Text.size) + .0125
        self.keyboard_graphic.y = (self.button_group.buttons[0].scale_x * Text.size)
        new_x = 0
        for i in range(12):
            e = Entity(parent=self.keyboard_graphic, model='quad', origin=(0,.5), scale=(1,4), color=color.white)
            new_x += .5
            if i in (1,3,6,8,10):
                e.z = -.1
                e.scale_x = .7
                e.scale_y = .6 * 4
                e.color = color.dark_gray

            if i == 5 or i == 12:
                new_x += .5

            e.x = new_x

        self.start_note_slider = Slider(0, 12, step=1, parent=self, scale=.5, height=Text.size*2)
        self.start_note_slider.bg.tooltip = tooltip=Tooltip('base note offset')
        self.start_note_slider.x = self.keyboard_graphic.x + .0125/2
        self.start_note_slider.y = (self.button_group.buttons[0].scale_x * Text.size) * 1.25
        self.start_note_slider.knob.text_entity.scale *= 2
        def set_base_note_offset():
            scale_changer.base_note_offset = self.start_note_slider.value
            self.visualize_scale()
        self.start_note_slider.on_value_changed = set_base_note_offset

        self.scale_rotation_slider = Slider(0, 12, step=1, parent=self, scale=.5, height=Text.size*2)
        self.scale_rotation_slider.bg.tooltip = tooltip=Tooltip('scale rotation')
        self.scale_rotation_slider.x = self.keyboard_graphic.x + .0125/2
        self.scale_rotation_slider.y = (self.button_group.buttons[0].scale_x * Text.size) * 1.75
        self.scale_rotation_slider.knob.text_entity.scale *= 2
        def set_scale_rotation():
            scale_changer.scale_rotation = self.scale_rotation_slider.value
            self.visualize_scale()
        self.scale_rotation_slider.on_value_changed = set_scale_rotation

        self.visualize_scale()





    def input(self, key):
        if key == 'left mouse down' and self.children and mouse.hovered_entity in self.button_group.buttons:
            scale_changer.pattern = [int(e) for e in mouse.hovered_entity.pattern if e != ' ']
            self.visualize_scale()

    def visualize_scale(self):
        # [destroy(c) for c in self.keyboard_graphic.children]
        # note_names = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

        for i in range(12):
            e = self.keyboard_graphic.children[i]
            e.color = color.white
            if i in (1,3,6,8,10):
                e.color = color.dark_gray

            # if (i-scale_changer.base_note_offset in scale_changer.final_offsets
            # or i+12-scale_changer.base_note_offset in scale_changer.final_offsets):
            #     e.color = lerp(e.color, color.cyan, .5)

        for i in range(len(scale_changer.pattern)):
            n = scale_changer.note_offset(i)
            if n >= 12:
                n -= 12
            self.keyboard_graphic.children[n].color = lerp(self.keyboard_graphic.children[n].color, color.cyan, .5)
        # print(scale_changer.final_offsets)


if __name__ == '__main__':
    app = Ursina()

sys.modules[__name__] = ScaleChangerMenu()


if __name__ == '__main__':
    import style
    # import keyboard
    t = time.time()
    # base.scale_changer = ScaleChanger()
    # base.scale_changer_menu = ScaleChangerMenu()
    # base.keyboard = Keyboard()
    print('---', time.time() - t)
    app.run()
