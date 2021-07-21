from ursina import *
from amvol_tooltip import AmvolTooltip as Tooltip

from ursina.prefabs.dropdown_menu import DropdownMenu
from ursina.prefabs.dropdown_menu import DropdownMenuButton as MenuButton
# from start_screen import StartScreen
if __name__ == '__main__':
    app = Ursina()

from style import *
import scale_changer
import scale_changer_menu
from note_section import NoteSection
# from note_section_grid import NoteSectionGrid as NoteSection
# from note_sheet import NoteSheet
# from note_recorder import NoteRecorder
import keyboard

window.color = color.color(24,.07,.28)
window.exit_button.scale = (.04, .02)
camera.orthographic = True
camera.fov = 6
camera.x = camera.fov * .875
camera.y = camera.fov * .375

import note_recorder
import note_sheet
bar = Entity(parent=camera.ui, model='quad', origin_y=-.5, y=-.5, z=-1, scale=(camera.aspect_ratio, .1), color=panel_color)
bar_border = Entity(parent=bar, model='quad', origin_y=-.5, y=1, z=-1, scale_y=.05, color=panel_color.tint(-.05), add_to_scene_entities=False)
keyboard_bg = Entity(parent=bar, model='quad', origin_y=-.5, y=0, z=-1, scale_y=.25, color=panel_color.tint(-.05))

stop_button = Button(scale=.035, world_parent=bar, x=-.028, y=.6, z=-1, model='quad', color=color.violet, tooltip=Tooltip('Stop'), on_click=note_sheet.stop)
play_button = Button(scale=.035, world_parent=bar, x=.028, y=.6, z=-1, model='quad', color=color.yellow, tooltip=Tooltip('Start'), on_click=note_sheet.play)

top_bar = Button(scale=(window.aspect_ratio, .02), model='quad', text='Amvol', origin_y=.5, y=.5, color=amvol_color, highlight_color=amvol_color)
top_bar.text_entity.scale *= .5
top_bar.text_entity.y = -.5


# class Amvol(Ursina):
#     def __init__(self, **kwargs):
#         super().__init__()

        # self.scale_changer = ScaleChanger()
        # self.scale_changer_menu = ScaleChangerMenu()
        # self.keyboard = Keyboard()


        # import keyboard
        # import instrument_menu
        # self.recent_files = ('wrgwrg', 'eth', 'ethkjiu', 'loojfi')
        # self.recent_files_buttons = [MenuButton(f) for f in self.recent_files]

        # self.dm = DropdownMenu('File', z=-.1, buttons=(
        #     MenuButton('New'),
        #     MenuButton('Open'),
        #     DropdownMenu('Open Recent', buttons=self.recent_files_buttons),
        #     MenuButton('Save'),
        #     MenuButton('Save As'),
        #     MenuButton('Options'),
        #     MenuButton('Exit', on_click=application.quit),
        #     )
        #     )
        # self.dm.scale /= self.dm.scale_y / self.top_bar.scale_y


# base.start_screen = StartScreen(z=-10, scale=1/1.5)
# start_screen.new_project_button.on_click()
# start_screen.input_field.text = 'yolo'
# start_screen.create_button.on_click()
if __name__ == '__main__':
    # from style import *
    # app = Amvol()
    # ref = Entity(parent=camera.ui, model='quad', scale_x=window.aspect_ratio, texture='amvol_ui_ref', z=-1, color=color.white33)
    # def input(key):
    #     ref.enabled = held_keys['tab']

    app.run()
