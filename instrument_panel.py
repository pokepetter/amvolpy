from ursina import *


class InstrumentPanel(Entity):
    def __init__(self):
        super().__init__()

        self.color = color.color(0,1,1,.2)
        # self.change_instrument_button = Button(
        #     color = color.green,
        #     scale = (.9, .2),
        #     text = 'instrument name'
        #     )

        # self.scale *= .5

        # self.attack_slider = Slider(z=-.1)
        # self.falloff_slider = Slider(y=-.01)
        for i in range(3):
            s = Slider(parent=self, x = -.45, y = i/3, z = -.1)
            s.scale *= .8




class Slider(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.origin = (-.5, 0)
        self.color = color.white
        self.scale_y = .1

        self.knob = Entity(
            parent = self,
            model = 'quad',
            color = color.pink,
            z = -.1,
            scale_x = .1
            )
        self.knob.slider = self

        self.tooltip = Tooltip()

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        if self.hovered and mouse.left:
            self.knob.x = mouse.point[0]
            self.tooltip.text_entity.text = round(self.knob.x, 2)
            self.tooltip.enabled = True

        else:
            self.tooltip.enabled = False


    @property
    def value(self):
        return self.knob.x


if __name__ == '__main__':
    app = Ursina()
    slider = InstrumentPanel()
    app.run()
