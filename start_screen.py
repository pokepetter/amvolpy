from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenuButton
from ursina.prefabs.input_field import InputField
from window_panel import WindowPanel, Space



class StartScreen(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui
            )

        self.bg = Panel(parent=self, z=.1, scale=(99,99), color=color.black33)
        self.input_field = InputField(height=1)

        def create():
            print('create')
            self.load(self.input_field.text)
            self.enabled = False

        self.create_button = Button(text='Create', color=color.yellow, scale_x=.5, on_click=create)

        self.name_prompt = WindowPanel(
            parent = self,
            title = 'Enter Project Name',
            content = (
                self.input_field,
                self.create_button,
                ),
            z = -1,
            scale_y=.03,
            color = color.amvol_color,
            popup = True,
            enabled = False
            )
        self.name_prompt.panel.color = color.panel_color


        def ask_for_name():
            original_scale = self.name_prompt.scale
            self.name_prompt.scale = 0
            self.name_prompt.enabled = True
            self.name_prompt.bg.world_scale = (99,99)
            self.name_prompt.fade_in(duration=.1)
            self.name_prompt.animate_scale(original_scale, duration=.2)
            self.name_prompt.content[0].editing = True

        self.new_project_button = Button('New Project', parent=self, color=color.amvol_color, scale=(.3, .05), y=.05, on_click=ask_for_name)
        self.open_button = Button('Open', parent=self, color=color.yellow, scale=(.3, .035), y=-.001)

        recent_files = open('recent_projects.txt').read().strip().split('\n')
        for i, f in enumerate(recent_files):
            Button(
                parent = self,
                text = f,
                hovered_color = color.orange,
                scale = (.4,.025),
                text_origin = (-.5, 0),
                y = -i*.025 -.075
                )


        for key, value in kwargs.items():
            setattr(self, key ,value)

    def load(self, name):
        camera.ui.animate_scale(camera.ui.scale / 1.5, curve=curve.in_out_expo, duration=.3)
        print('load:', name)

if __name__ == '__main__':
    app = Ursina()
    panel_color =   color.color(32,.2,.25)
    record_color =  color.color(0,.68,.62)
    color.yellow =  color.color(31,.68,.62)
    color.violet =  color.color(292,.68,.62)
    Button.color =  color.color(22,.48,.42)
    amvol_color =   color.color(56,.28,.38)

    color.amvol_color = amvol_color
    color.panel_color = panel_color
    color.record_color = record_color
    StartScreen()
    app.run()
