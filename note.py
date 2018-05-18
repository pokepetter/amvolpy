from pandaeditor import *
import snapsettings


class Note(Entity):
    def __init__(self):
        super().__init__()
        self.model = 'quad'
        self.rotation_z = 45
        # self.color = color.clear
        self.scale *= .05
        self.z = -.1
        self.collider = 'box'
        self.model = None

        self.circle = Entity(
            model = 'circle_16',
            parent = self,
            color = color.lime,
            z = -.1,
        )

        self.length_indicator = Entity(
            parent = self,
            model = 'quad',
            origin = (-.5, 0),
            rotation_z = -45,
            color = self.circle.color,
            scale_y = .2
        )

        self.press_time = 0
        print('------------------')
        self.max_circle_size = self.circle.scale
        self.length = 0
        self.strength = .6


    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        value = max(0, value)
        self._length = value
        self.length_indicator.scale_x = value * 10

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self, value):
        self._strength = clamp(value, .2, 1)
        self.circle.scale = Point3(1,1,1) * (self._strength + .2) * .5


    def update(self, dt):
        self.press_time += dt
        if self.press_time >= snapsettings.add_length_snap:
            if mouse.left and self.hovered:
                self.length += snapsettings.add_length_snap
            if mouse.right and self.hovered:
                self.length -= snapsettings.add_length_snap

            self.press_time = 0


    def input(self, key):
        if self.hovered:
            if key == 'scroll up':
                self.strength += .2
            elif key == 'scroll down':
                self.strength -= .2

            if key == 'right mouse down':
                destroy(self)