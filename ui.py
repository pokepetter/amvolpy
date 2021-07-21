from ursina import *
import notesheet
import note_recorder
from amvol_tooltip import AmvolTooltip as Tooltip
from ursina.prefabs.dropdown_menu import DropdownMenu
from ursina.prefabs.dropdown_menu import DropdownMenuButton as MenuButton



panel_color =   color.color(32,.2,.25)
record_color =  color.color(0,.68,.62)
color.yellow =  color.color(31,.68,.62)
color.violet =  color.color(292,.68,.62)
Button.color =  color.color(22,.48,.42)
amvol_color =   color.color(56,.28,.38)

color.amvol_color = amvol_color
color.panel_color = panel_color
color.record_color = record_color



bar = Entity(parent=camera.ui, model='quad', origin_y=-.5, y=-.5, z=-1, scale=(camera.aspect_ratio, .1), color=panel_color)
bar_border = Entity(parent=bar, model='quad', origin_y=-.5, y=1, z=-1, scale_y=.05, color=panel_color.tint(-.05))
keyboard_bg = Entity(parent=bar, model='quad', origin_y=-.5, y=0, z=-1, scale_y=.25, color=panel_color.tint(-.05))

record_button = Button(scale=.055, world_parent=bar, y=.6, z=-1, color=record_color, tooltip=Tooltip('Record'), on_click=note_recorder.start_recording)
stop_recording_button = Button(scale=.055, world_parent=bar, y=.6, z=-1.1, color=color.lime, tooltip=Tooltip('Stop recording'), on_click=note_recorder.stop_recording, enabled=False)
stop_button = Button(scale=.035, world_parent=bar, x=-.028, y=.6, z=-1, color=color.violet, tooltip=Tooltip('Stop'), on_click=notesheet.stop)
play_button = Button(scale=.035, world_parent=bar, x=.028, y=.6, z=-1, color=color.yellow, tooltip=Tooltip('Start'), on_click=notesheet.play)

top_bar = Button(scale=(window.aspect_ratio, .02), model='quad', text='Amvol', origin_y=.5, y=.5, color=amvol_color)
top_bar.text_entity.scale *= .5
top_bar.text_entity.y = -.5
recent_files = ('wrgwrg', 'eth', 'ethkjiu', 'loojfi')
recent_files_buttons = [MenuButton(f) for f in recent_files]

dm = DropdownMenu('File', position=window.top_left, z=-.1, buttons=(
    MenuButton('New'),
    MenuButton('Open'),
    DropdownMenu('Open Recent', buttons=recent_files_buttons),
    MenuButton('Save'),
    MenuButton('Save As'),
    MenuButton('Options'),
    MenuButton('Exit', on_click=application.quit),
    )
    )
dm.scale /= dm.scale_y / top_bar.scale_y


# if __name__ == '__main__':
#     app = Ursina()
#
#     app.run()
