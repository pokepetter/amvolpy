from ursina import *


class Note:

    default_length = .125

    def __init__(self, x, y, length=default_length, strength=1):
        self.x = x
        self.y = y
        self.length = length
        self.strength = strength

class LoopButton(Draggable):
    def __init__(self, note_section):
        super().__init__(model='quad', parent=note_section, lock_y=True, scale=(.05, 1), origin_y=.5, position=(1,1,-.1), color=color.green, min_x=0)
        self.note_section = note_section


    def drop(self):
        self.note_section.end_button.world_parent = scene
        self.note_section.scale_x = self.x * self.note_section.scale_x
        self.note_section.scale_x = max(self.note_section.scale_x, .05)
        self.note_section.scale_x = int(self.note_section.scale_x * 16) / 16
        self.x = 1
        self.note_section.end_button.world_scale_x = .05
        self.note_section.loop_button.world_scale_x = .05
        self.note_section.end_button.world_parent = self.note_section

        self.note_section.loops = self.x / self.note_section.end_button.x
        self.note_section.draw_notes()


class EndButton(Draggable):
    def __init__(self, note_section):
        super().__init__(model='quad', parent=note_section, lock_y=True, scale=(.05, .1), origin_y=.5, position=(1,1,-.2), color=color.orange, min_x=0)
        self.note_section = note_section
    def drop(self):
        self.note_section.loop_button.world_parent = scene
        self.note_section.scale_x = self.x * self.note_section.scale_x
        self.note_section.scale_x = max(self.note_section.scale_x, .05)
        self.note_section.scale_x = int(self.note_section.scale_x * 16) / 16
        self.x = 1
        self.note_section.end_button.world_scale_x = .05
        self.note_section.loop_button.world_scale_x = .05
        self.note_section.loop_button.world_parent = self.note_section

        if self.x > self.note_section.loop_button.x:
            self.note_section.loop_button.x = self.x
            self.note_section.draw_notes()
        self.note_section.loop_button.drop()


class NoteSection(Draggable):
    def __init__(self, **kwargs):
        super().__init__(parent=scene, model='quad', color=color.black33)
        self.highlight_color = self.color
        self.origin = (-.5, -.5)

        self.notes = list()
        self.note_parent = Entity(parent=self, color=color.lime, z=-.1, model=Mesh(vertices=(), mode='line', thickness=camera.fov*2))
        self.note_loops = Entity(parent=self.note_parent, color=color.gray, z=-.1, model=Mesh(vertices=(), mode='line', thickness=camera.fov*2))
        self.loop_lines = Entity(parent=self, color=color.azure, z=-.1, model=Mesh(vertices=(), mode='line', thickness=camera.fov*.5))
        self.height = 64
        self.scale_y = self.height / 32
        # self.grid = Entity(parent=self, model=Grid(4, self.height), z=-.1, color=color.dark_gray)
        self.scroll = 0
        self.scroll_speed = 5
        self.scroll_indicator = Entity(parent=self, model='quad', scale=(1/64, 1/16), color=color.gray, origin=(.5, -.5))
        self.loops = 1
        self.loop_number = Text(parent=self, text='1', origin=(.6, -.4), scale=(3,3/self.scale_y), color=color.white33, y=.1)
        self.end_button = EndButton(self)
        self.loop_button = LoopButton(self)

        self.current_note = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        if held_keys['control']:
            super().update()

        if self.hovered and mouse.left and self.current_note:   # drag note length
            self.current_note.length = Note.default_length + mouse.delta[0] * 8
            self.current_note.length = int(self.current_note.length * 16) / 16
            self.draw_notes()


    def input(self, key):
        super().input(key)
        if self.hovered:
            x = (mouse.point[0] / self.end_button.x) * self.scale_x / self.loops
            # adjust for clicking in a loop
            x -= math.floor(mouse.point[0] * self.loops) * (self.end_button.x * self.scale_x)

            y = math.floor(mouse.point[1] * self.height) + self.scroll

            if key == 'left mouse down':
                # print(int(mouse.point[1] * 32) /32)
                self.current_note = Note(x,y)
                self.notes.append(self.current_note)
                self.draw_notes()

            if key == 'right mouse down':
                self.notes = [n for n in self.notes if n.y != y or n.x > x or n.x+n.length <= x]
                self.draw_notes()

            if key == 'left mouse up':
                self.current_note = None

            if key in ('arrow up', 'arrow up hold', 'scroll up'):
                self.scroll += self.scroll_speed
            if key in ('arrow down', 'arrow down hold', 'scroll down'):
                self.scroll -= self.scroll_speed

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value


    @property
    def scroll(self):
        return self._scroll

    @scroll.setter
    def scroll(self, value):
        value = clamp(value, 0, 128-self.height)
        self._scroll = value
        self.draw_notes()
        self.scroll_indicator.text = str(value)
        t = value/128 * 2
        self.scroll_indicator.y = lerp(0, 1-self.scroll_indicator.scale_y, t)
        # print(self.scroll_indicator.y)


    def add_note(self, x, y, length=1/4, strength=1):
        self.notes.append(Note(x, y, length, strength))


    def draw_notes(self):
        note_verts = list()
        loop_note_verts = list()
        loop_lines = list()
        width = self.end_button.x * self.scale_x

        for i in range(0, math.ceil(self.loops)):
            if i > 0 and self.loops > 1:
                loop_lines += ((i/self.loops,0,0), (i/self.loops,1,0))

            for n in self.notes:
                if (n.y >= self.scroll and n.y < self.height + self.scroll
                and n.x <= min(width, self.loop_button.x*self.scale_x)
                and (i / self.loops) + (n.x / self.loops / width)<= 1
                ):
                    y = (n.y/self.height)+(1/self.height/2)
                    line = (
                        ((i/self.loops) + (n.x/self.loops/width), y, 0),
                        ((i/self.loops) + (n.x/self.loops/width) + n.length/self.loops/width, y, 0),
                        )

                    if i == 0:
                        note_verts += line
                    elif self.loops > 1:
                        loop_note_verts += line


        self.note_parent.y = -self.scroll / self.height
        self.note_parent.enabled = bool(note_verts)
        self.note_parent.model.vertices = note_verts
        self.note_parent.model.generate()

        self.note_loops.enabled = bool(loop_note_verts)
        self.note_loops.model.vertices = loop_note_verts
        self.note_loops.model.generate()

        self.loop_lines.enabled = bool(loop_lines)
        self.loop_lines.model.vertices = loop_lines
        self.loop_lines.model.generate()

        self.loop_number.text = round(self.loops, 1)
        self.loop_number.world_scale = 3



if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 4
    camera.position = (.5,.5)
    note_section_parent = Entity()
    note_section = NoteSection(parent=note_section_parent)
    note_section.loop_button.x = 2
    note_section.loop_button.drop()

    for i in range(4):
        note_section.add_note(i/4, i*2, 1/4, 1)

    note_section.draw_notes()

    def input(key):
        if mouse.hovered_entity == None:
            if key == 'scroll down':
                note_section_parent.scale_x -= .1
                note_section_parent.scale_x = max(.025, note_section_parent.scale_x)
            if key == 'scroll up':
                note_section_parent.scale_x += .1

    app.run()
