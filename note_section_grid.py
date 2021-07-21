from ursina import *

from note_section import NoteSection
from note import Note
import math

class NoteSectionGrid(NoteSection):
    def __init__(self, height=16, **kwargs):
        super().__init__(height=height, **kwargs)
        self.require_key = 'shift'
        # self.note_grid = [[0 for y in range(self.height)] for x in range(int(self.scale_x / self.loops * 16))]
        # self.note_grid = [[0 for x in range(int(self.scale_x / self.loops * 16))] for y in range(self.height)]
        self.note_grid = [[0 for x in range(512)] for y in range(self.height)]
        self.octave_offset = 2

        self.ui_parent = Entity(parent=self)
        ui_parent = self.ui_parent
        self.grab_bar = Draggable(parent=self, scale_y=1/height, origin=(-.5,-.5,-.1), color=color.gray, y=1)
        self.grab_bar.world_parent = self.parent
        self.world_parent = self.grab_bar


        class CustomButton(Button):
            def __init__(self, **kwargs):
                super().__init__(parent=ui_parent, model='quad', color=color.gray, y=1, origin=(-.5,-.5), scale=1/height)
                for key, value in kwargs.items():
                    setattr(self, key ,value)

        self.speed = .25
        self.speed_menu = ButtonList(
            {
            '16ths' : Func(setattr, self, 'speed', 1),
            '8ths' : Func(setattr, self, 'speed', 1/2),
            '4ths' : Func(setattr, self, 'speed', 1/4),
            '3rds' : Func(setattr, self, 'speed', 1/6),
            '2nds' : Func(setattr, self, 'speed', 1/8),
            'whole notes' : Func(setattr, self, 'speed', 1/16),
            },
            fit_height=True,
            enabled=False,
        )




        self.play_button =          CustomButton(text='>', color=color.azure, on_click=self.play, tooltip=Tooltip('play'))
        self.instrument_button =    CustomButton(text='i', color=color.orange, tooltip=Tooltip('instrument'), on_click=self.open_instrument_menu)
        self.attack_button =        CustomButton(text='/', tooltip=Tooltip('attack'))
        self.falloff_button =       CustomButton(text='\\', tooltip=Tooltip('falloff'))
        self.mute_button =          CustomButton(text='m', tooltip=Tooltip('mute'))
        self.speed_button =         CustomButton(text='16', on_click=Func(setattr, self.speed_menu, 'enabled', True))
        self.octave_button_down =   CustomButton(text='v', on_click=self.decrease_octave_offset, tooltip=Tooltip('octave offset'))
        self.octave_indicator =     CustomButton(text='0', tooltip=Tooltip('octave offset'))
        self.octave_button_up =     CustomButton(text='^', on_click=self.increase_octave_offset, tooltip=Tooltip('octave offset'))

        for i, e in enumerate(self.ui_parent.children):
            e.x = 1/height * i
            e.text_entity.scale= 2



    def convert_grid_to_notes(self):
        self.notes = []
        for y in range(len(self.note_grid)):
            current_note = None

            for x, n in enumerate(self.note_grid[y]):
                if n == 1:
                    if not current_note:
                        current_note = Note(x=x/16, y=y, length=1/16)
                        self.notes.append(current_note)
                    else:
                        current_note.length += 1/16
                else:
                    current_note = None
        self.draw_notes()


    def input(self, key):
        pass # override original input function


    def update(self):
        # if mouse.hovered_entity:
        #     if self.hovered or mouse.hovered_entity.has_ancestor(self):
        #         self.ui_parent.enabled = True
        #     else:
        #         self.ui_parent.enabled = False
        # else:
        #     self.ui_parent.enabled = False


        if held_keys['shift']:
            return

        if self.hovered:
            x = (mouse.point[0] / self.end_button.x) * self.scale_x / self.loops
            # adjust for clicking in a loop
            x -= math.floor(mouse.point[0] * self.loops) * (self.end_button.x * self.scale_x)
            y = math.floor(mouse.point[1] * self.height) + self.scroll
            x = int(x*16)
            # print('--', y, x)

            if mouse.left:
                # print(self.note_grid[y][x])
                if self.note_grid[y][x] == 0:
                    self.note_grid[y][x] = 1

                self.convert_grid_to_notes()

            if mouse.right:
                if self.note_grid[y][x] > 0:
                    self.note_grid[y][x] = 0

                self.convert_grid_to_notes()

        self.end_button.world_scale = .075
        self.loop_button.world_scale_x = .075

        self.ui_parent.world_scale = 1


    def decrease_octave_offset(self):
        self.octave_offset -= 1

    def increase_octave_offset(self):
        self.octave_offset += 1


    @property
    def octave_offset(self):
        return self._octave_offset

    @octave_offset.setter
    def octave_offset(self, value):
        self._octave_offset = value
        self.octave_indicator.text_entity.text = str(value)




if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    import keyboard
    t = time.time()
    note_section = NoteSectionGrid(size=1, loops=1, position=(-.5,-.5))
    note_section.selected = True
    print('----', time.time() - t)
    camera.fov = 3

    # for i, y in enumerate(range(24, 8, -8)):
    #     note_section.add_note(4, y, 1, 1)

    note_section.draw_notes()
    app.run()
