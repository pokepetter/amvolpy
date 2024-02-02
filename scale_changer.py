from ursina import *




class ScaleChanger(Entity):
    def __init__(self):
        super().__init__()
        self.base_note_offset = 0

        self.final_offsets = list()

        self.patterns = {
            'chromatic' : (1,1,1,1,1,1,1,1,1,1,1,1),

            'heptatonic' : (2,2,1,2,2,2,1),
            'natural minor' : (2,1,2,2,1,2,2),
            'dorian' : (2,1,2,2,2,1,2),

            'hexadiatonic' : (2,2,1,2,2,3),

            'whole tone' : (2,2,2,2,2,2),

            'minor pentatonic' : (3,2,2,3,2),
            'major pentatonic' : (2,2,3,2,3),
            'ritsusen' : (2,3,2,2,3),

            'phrygian dominant' : (1,3,1,2,1,2,2),
            }
        # self.pattern = (2, 2, 1, 2, 2, 3)
        # self.pattern = (1,)*12
        self.pattern = (2,1,2,2,2,1,2)
        self.scale_rotation = 0
        # self.pattern = (3,2,2,3,2) # minor pentatonic

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        # self._pattern = value[self.scale_rotation:]+value[:self.scale_rotation] #rotate scale
        self._pattern = value

        self.final_offsets = list()
        cumulative = 0

        for e in self._pattern:
            cumulative += e
            self.final_offsets.append(cumulative)


    @property
    def base_note_offset(self):
        return self._base_note_offset

    @base_note_offset.setter
    def base_note_offset(self, value):
        self._base_note_offset = value

    @property
    def scale_rotation(self):
        return self._scale_rotation

    @scale_rotation.setter
    def scale_rotation(self, value):
        self._scale_rotation = value
        # print('base note offset:----', value)
        rotated_pattern = self.pattern[value:]+self.pattern[:value] #rotate scale

        self.final_offsets = list()
        cumulative = 0

        for e in rotated_pattern:
            cumulative += e
            self.final_offsets.append(cumulative)


    def note_offset(self, y, normalize_within_octave=False):
        if y == 0:
            # print("no note on 0")
            return 0

        sL = (y-1) / (len(self.pattern))
        filled_octaves = int(sL)
        offset = self.final_offsets[y - (filled_octaves * (len(self.pattern))) - 1]

        if normalize_within_octave:
            if offset + self.base_note_offset > 12:
                return (offset + self.base_note_offset) - 12

            return offset + self.base_note_offset

        return filled_octaves * 12 + offset + self.base_note_offset



if __name__ == '__main__':
    app = Ursina()
scale_changer = ScaleChanger()
sys.modules[__name__] = scale_changer
if __name__ == '__main__':

    pattern = scale_changer.patterns['heptatonic']

    buttons = []
    for oct in range(3):
        for i, n in enumerate(('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')):
            b = Button(scale=.05, text=n, x=-.7+(i*.05) + (oct*.05*12), color=color.white, text_color=color.black)
            buttons.append(b)
            if n.endswith('#'):
                b.color=color.black
                b.text_color=color.white
                b.y = .025

    for i, b in enumerate(buttons):
        n = scale_changer.note_offset(i)
        print(n)
        if n < len(buttons):
            buttons[n].color = color.azure
            buttons[n].text_color = color.white


    app.run()




        # ScaleChanger()
    # import keyboard
    # ScaleChangerMenu()
    # origin=
