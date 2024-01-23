from ursina.scripts.property_generator import generate_properties_for_class
@generate_properties_for_class()
class Audio2:
    def __init__(self, sound_file_name, left_sound='', right_sound='', autoplay=True, auto_destroy=False, loop=False, volume=1, pitch=1, balance=0):
        # super().__init__(**kwargs)
        self.left_sound = left_sound
        if not left_sound:
            self.left_sound = Audio(f'{sound_file_name}_left')

        self.right_sound = right_sound
        if not right_sound:
            self.right_sound = Audio(f'{sound_file_name}_right')
        # print('-------------------', self.left_sound, self.right_sound)

        if autoplay:
            self.play()

        if auto_destroy:
            invoke(self.stop, destroy=True, delay=self.length)

        self.balance = balance
        self.volume = volume


    def balance_setter(self, value):
        self._balance = value

    def volume_setter(self, value):
        self._volume = value
        value = self.balance + .5
        self.right_sound.volume = lerp(0, .5, value) * self.volume
        self.left_sound.volume = lerp(.5, 0, value) * self.volume
        # self.balance = self.balance

    def pitch_setter(self, value):
        self._pitch = value
        self.left_sound.pitch = value
        self.right_sound.pitch = value

    def loop_setter(self, value):
        self._loop = value
        self.left_sound.loop = value
        self.right_sound.loop = value

    def autoplay_setter(self, value):
        self._autoplay = value
        self.left_sound.autoplay = value
        self.right_sound.autoplay = value

    def auto_destroy_setter(self, value):
        self._auto_destroy = value
        self.left_sound.auto_destroy = value
        self.right_sound.auto_destroy = value


    def play(self):
        self.left_sound.play()
        self.right_sound.play()

    def fade_out(self, **kwargs):
        self.left_sound.fade_out(**kwargs)
        self.right_sound.fade_out(**kwargs)
