from ursina import *

class AmvolTooltip(Tooltip):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __init__(self, text='', **kwargs):
        super().__init__(
            text,
            margin = (.5, .5),
            enabled = False,
            # background = True,
            **kwargs
            )

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.create_background(padding=self.size/2, radius=self.size/4, color=color.brown)
        # self.background_border = duplicate(self._background)
        # self.background_border.x = 1

if __name__ == '__main__':
    app = Ursina()
    tt = AmvolTooltip('Tooltip')
    tt.enabled = True
    app.run()
