from ursina import *


class InstrumentMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, enabled=False)


        self.target_note_section = None     # set by note_section instance
        self.bg = Button(parent=self, z=1, model='quad', world_scale=(99,99,1), color=color.black66, highlight_color=color.black66)
        self.bg.on_click = Func(setattr, self, 'enabled', False)
        self.instrument_folder = application.asset_folder / 'samples'
        self.button_list = ButtonList(dict(), parent=self, button_height=1.25, x=.5*0, fit_height=False)
        self.up_button = Button(parent=self, scale=.05, text='^', y=.45, origin=(.5,.5))

        self.go_to_path(self.instrument_folder)

        for key, value in kwargs.items():
            setattr(self, key ,value)



    def go_to_path(self, path):
        button_dict = dict()
        unique_names = list()

        if path == self.instrument_folder:
            self.up_button.enabled = False
        else:
            self.up_button.enabled = True
            self.up_button.on_click = Func(self.go_to_path, path.parent)

        for folder in [x for x in path.iterdir() if x.is_dir()]:
            print('-......', folder.name)
            button_dict[f'<cyan>{folder.name}<default>'] = Func(self.go_to_path, folder)


        for ft in ('.mp3', '.ogg', '.wav'):
            for f in path.glob('*' + ft):

                if not ('[') in f.stem:
                    continue

                name_without_tags = f.stem.split('[', 1)[0]

                if not name_without_tags in unique_names:
                    unique_names.append(name_without_tags)

        for i, name in enumerate(unique_names):
            button_dict[name] = Func(self.set_instrument, name)


        self.button_list.button_dict = button_dict
        self.button_list.highlight.color = color.yellow.tint(-.5)


    def set_instrument(self, name):
        if self.target_note_section is None:
            print('error: target_note_section is None')
            return

        # print('setting intr from intr menu:', name)
        self.target_note_section.instrument = name
        # self.target_note_section.color = color.blue
        # base.keyboard.instrument = name



    def on_double_click(self):
        self.enabled = False
    #     if key == 'scroll down':
    #         self.button_list_parent.x -= .1
    #     if key == 'scroll up':
    #         self.button_list_parent.x += .1
    #
    #     max_scroll = self.button_list_parent.children[0].scale_x * len(self.button_list_parent.children)
    #     print('...', max_scroll)
    #     self.button_list_parent.x = clamp(self.button_list_parent.x, -max_scroll+.75, -.5)




if __name__ == '__main__':
    app = Ursina()
    import time
    t = time.time()
    camera.orthographic = True
    import keyboard
    instrument_menu = InstrumentMenu(target_note_section=keyboard.fallback_ns)
    instrument_menu.enabled = True
    # from ursina.prefabs.file_browser import FileBrowser
    # file_browser = FileBrowser(start_path=application.asset_folder / 'instruments')


    def input(key):
        if key == 'space':
            instrument_menu.enabled = True

    # sys.modules['instrument_menu'] = InstrumentMenu()
    print('-------', time.time() - t)
    app.run()
