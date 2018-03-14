from pandaeditor import *

class ScaleChanger(object):

    def __init__(self):
        self.base_note_offset = 0
        self.scale_rotation = 0

        self.final_offsets = list()
        self.scale = (2, 2, 1, 2, 2, 3)


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



sys.modules[__name__] = ScaleChanger()

if __name__ == '__main__':
    import scalechanger
    print(1, scalechanger.note_offset(1))
    print(5, scalechanger.note_offset(5))
    print(9, scalechanger.note_offset(9))
