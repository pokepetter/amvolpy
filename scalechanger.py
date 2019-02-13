from ursina import *

class ScaleChanger(Entity):

    def __init__(self):
        super().__init__()
        self.base_note_offset = 0
        self.scale_rotation = 0

        self.final_offsets = list()
        self.scale = (2, 2, 1, 2, 2, 3)
        self.scale = (1,)*12
        # self.scale = (2,1,2,2,2,1,2)


    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value[self.scale_rotation:]+value[:self.scale_rotation] #rotate scale

        self.final_offsets = list()
        cumulative = 0

        for e in self._scale:
            cumulative += e
            self.final_offsets.append(cumulative)

        self.visalize_scale()

    @property
    def base_note_offset(self):
        return self._base_note_offset

    @base_note_offset.setter
    def base_note_offset(self, value):
        self._base_note_offset = value
        self.visalize_scale()

    @property
    def scale_rotation(self):
        return self._scale_rotation

    @scale_rotation.setter
    def scale_rotation(self, value):
        self._scale_rotation = value
        self.visalize_scale()


    def note_offset(self, y, normalize_within_octave=False):
        if y == 0:
            print("no note on 0")
            return 0

        sL = (y-1) / (len(self.scale))
        filled_octaves = int(sL)
        offset = self.final_offsets[y - (filled_octaves * (len(self.scale))) - 1]

        if normalize_within_octave:
            if offset + self.base_note_offset > 12:
                return (offset + self.base_note_offset) - 12

            return offset + self.base_note_offset

        # print("y:", y)
        return filled_octaves * 12 + offset + self.base_note_offset


    def input(self, key):
        if key.isdigit():
            if held_keys['shift']:
                self.base_note_offset = int(key)
                print('base note offset:', self.base_note_offset)

            if held_keys['alt']:
                self.scale_rotation = int(key)
                printvar('scale_rotation:', self.scale_rotation)


    def visalize_scale(self):
        if hasattr(self, 'keyboard_graphic'):
            destroy(self.keyboard_graphic)

        # draw keyboard
        self.keyboard_graphic = Entity()
        self.keyboard_graphic.scale *= .5
        new_x = 0
        for i in range(12):
            e = Entity(parent=self.keyboard_graphic, model='quad', origin=(0,.5), scale=(1,4), texture='white_cube')
            new_x += .5
            if i in (1,3,6,8,10):
                e.z = -.1
                e.scale_x *= .7
                e.scale_y *= .6
                e.color = color.dark_gray

            if i == 5 or i == 12:
                new_x += .5

            e.x = new_x

            if i-self.base_note_offset in self.final_offsets or i+12-self.base_note_offset in self.final_offsets:
                e.color = lerp(e.color, color.cyan, .5)


if __name__ == '__main__':
    app = Ursina()
    ScaleChanger()
    app.run()
    # import scalechanger
#     print(1, scalechanger.note_offset(1))
#     print(5, scalechanger.note_offset(5))
#     print(9, scalechanger.note_offset(9))
