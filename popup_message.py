from ursina import *



class PopupMessage(WindowPanel):
    
    def __init__(self, title='Warning', message='', **kwargs):

        b = Button('OK')
        text = Text(message, scale=.75)

        super().__init__(
            title = title,
            content = (text, b),
            popup = True,
            z = -10
        )

        b.on_click = self.bg.on_click


        for key, value in kwargs.items():
            setattr(self, key, value)



if __name__ == '__main__':
    app = Ursina()
    PopupMessage()
    app.run()
