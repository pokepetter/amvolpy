from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenuButton
from ursina.prefabs.input_field import InputField
from ursina.prefabs.window_panel import WindowPanel, Space
import amvol


class StartScreen(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=camera.ui
            )

        self.bg = Panel(parent=self, z=.1, scale=(99,99), color=color.black33)
        self.input_field = InputField(height=1)

        def create():
            amvol.create(self.input_field.text)

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


        def name_prompt_close():
            for input_field in [c for c in self.name_prompt.content if isinstance(c, InputField)]:
                input_field.text = input_field.start_text

        self.name_prompt.close = name_prompt_close
        original_name_promt_scale = self.name_prompt.scale

        def ask_for_name():
            self.name_prompt.scale = 0
            self.name_prompt.enabled = True
            self.name_prompt.bg.enabled = True
            self.name_prompt.animate_scale(original_name_promt_scale, duration=.2)
            self.input_field.editing = True

        self.new_project_button = Button('New Project', parent=self, color=color.amvol_color, scale=(.3, .05), y=.05, on_click=ask_for_name)

        self.load_menu = FileBrowser(parent=self, path=Path('amvol_projects'), file_types=('.amvol'), enabled=False)
        def on_submit(selection):
            for b in [e for e in selection if e.path.is_file()]:
                amvol.load(b.path)

        self.load_menu.on_submit = on_submit


        def open_load_menu():
            self.load_menu.enabled = True

        self.open_button = Button('Open', parent=self, color=color.yellow, scale=(.3, .035), y=-.001, on_click=open_load_menu)


        class OpenRecentButton(Button):
            def on_click(self):
                amvol.load(self.path)

        recent_files = open('recent_projects.txt').read().strip().split('\n')
        for i, f in enumerate(recent_files):
            OpenRecentButton(
                parent = self,
                text = Path(f).stem,
                hovered_color = color.orange,
                scale = (.4,.025),
                # text_origin = (-.5, 0),
                y = -i*.025 -.075,
                path = Path(f)
                )


        for key, value in kwargs.items():
            setattr(self, key ,value)


    def on_enable(self):
        import keyboard
        keyboard.enabled = False
        camera.ui.animate_scale(camera.ui.scale * 1.5, curve=curve.in_out_expo, duration=.15, delay=.05)


    def close(self):
        import keyboard
        camera.ui.animate_scale(camera.ui.scale / 1.5, curve=curve.in_out_expo, duration=.3)
        keyboard.enabled = True
        self.enabled = False




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
    ss = StartScreen()
    # invoke(ss.close, delay=4)
    app.run()
