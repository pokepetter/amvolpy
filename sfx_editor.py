from ursina import *
import json
from ursina.scripts.property_generator import generate_properties_for_class

app = Ursina(borderless=False)


from ursina.prefabs import ursfx
from ursina.prefabs.ursfx import UrsfxGUI
window.color = color._8
guis = [UrsfxGUI(enabled=True, x=(-.5*window.aspect_ratio)+.2+(i*.36), y=.15, z=-1, scale=.75) for i in range(5)]
for i, e in enumerate(guis):
    e.background_panel.color = hsv(i*60, .5,.2,1)

SELECTED = None
BLOCKS = []
CURRENT_PATH = None


@generate_properties_for_class()
class Block(Draggable):
    def __init__(self, **kwargs):
        super().__init__(**(kwargs | dict(lock=(0,1,1), origin=(-.5,0), min_x=-.5, max_x=.5, scale=(.2,.07), color=color.azure)))
        self.mute_button = Button(parent=self, model='circle', origin=(.5,0), position=(.95,-.0,-.01), color=color.blue, world_scale=.9, text_size=.5, text='mute', on_click=self.toggle_muted)
        self.muted = False
        Entity(parent=self, model='quad', world_scale=.1)

    def toggle_muted(self):
        self.muted = not self.muted

    def muted_setter(self, value):
        self._muted = value
        if not value:
            self.mute_button.text = 'mute'
            self.mute_button.color = color.blue
        else:
            self.mute_button.text = 'unmute'
            self.mute_button.color = color.orange

for i in range(4):
    block = Block(text=f'{i}', x=-.5+(i*.3), y=-.1+(-i*.075))

    # d.on_click = Func(select, d)
    block.gui = guis[i]
    BLOCKS.append(block)

# bg = Entity(parent=camera.ui, model='quad', position=(-.5,0,1), origin=(-.5,.5), scale=(1,.5), color=color._16)
bg = Entity(parent=camera.ui, model='quad', z=1, color=color._16)


def play_all():
    for i, e in enumerate(BLOCKS):
        if not e.muted:
            invoke(e.gui.play, delay=e.x+.5)


def input(key):
    combined_key = input_handler.get_combined_key(key)
    if key == 'space':
        play_all()

    elif combined_key == 'control+s':
        if CURRENT_PATH:
            save_file(CURRENT_PATH)
        else:
            save_menu.enabled = True

    elif combined_key == 'control+shift+s':
        save_menu.enabled = True

    elif combined_key == 'control+o':
        load_menu.enabled = True


def pitch_all(diff):
    for e in guis:
        e.pitch_slider.value += diff

b = Button('P-', scale=.05, on_click=Func(pitch_all, -1),position=window.bottom+Vec2(-.2-.05,.05), color=color.turquoise)
b = Button('P+', scale=.05, on_click=Func(pitch_all, +1), position=window.bottom+Vec2(-.2+.025,.05), color=color.turquoise)

volume_indicator = Text('0', position=window.bottom+Vec2(-.05,.1))
VOLUME_CHANGE = 0
def volume_all(diff):
    global VOLUME_CHANGE
    VOLUME_CHANGE += diff
    volume_indicator.text = str(round(VOLUME_CHANGE,2))
    for e in guis:
        e.volume_slider.value += diff

b = Button('V-', scale=.05, on_click=Func(volume_all, -.05), position=window.bottom+Vec2(-.05,.05), color=color.magenta)
b = Button('V+', scale=.05, on_click=Func(volume_all, +.05), position=window.bottom+Vec2(.025,.05), color=color.magenta)

from ursina.prefabs.file_browser import FileBrowser
load_menu = FileBrowser(z=-10, file_types=['.pse', ], enabled=False)
@(lambda f: setattr(load_menu, 'on_submit', f))
def on_submit(paths):
    load_file(paths[0])


from ursina.prefabs.file_browser_save import FileBrowserSave
save_menu = FileBrowserSave(z=-10, file_type='.pse', enabled=False)
@(lambda f: setattr(save_menu, 'on_submit', f))
def on_submit(path):
    global CURRENT_PATH
    save_file(path)
    CURRENT_PATH = path

print('-----------args:', sys.argv)
if len(sys.argv) > 1:
    load_file(Path(sys.argv[1]))


def save_file(path):
    print('save file:', path)
    # if not path.endswith('.')

    data = {
        'sounds' : [e.gui.recipe for e in BLOCKS],
        'positions' : [(round(e.x,3), round(e.y,3)) for e in BLOCKS],
        'muted' : [e.muted for e in BLOCKS],
    }
    with path.open('w') as file:
        json.dump(data, file, indent=4)


def load_file(path):
    global CURRENT_PATH

    with path.open('r') as file:
        data = json.load(file)
        for i, code in enumerate(data['sounds']):
            BLOCKS[i].gui.paste_code(code)

        for i, pos in enumerate(data['positions']):
            BLOCKS[i].position = pos

        for i, is_muted in enumerate(data['muted']):
            BLOCKS[i].muted = is_muted

    CURRENT_PATH = path


# camera.orthographic = True
# camera.fov = 15
# camera.x = 10
EditorCamera()
app.run()
