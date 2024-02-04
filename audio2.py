from ursina.scripts.property_generator import generate_properties_for_class
@generate_properties_for_class()
class Audio2:
    def __init__(self, sound_file_name='', left_sound='', right_sound='', autoplay=True, auto_destroy=False, loop=False, volume=1, pitch=1, balance=0):
        # super().__init__(**kwargs)
        # if sound_file_name:
        #     self.left_sound = Audio(f'{sound_file_name}', volume=volume/2)
        #     self.right_sound = Audio(f'{sound_file_name}', volume=volume/2)

        self.left_sound = left_sound
        if not left_sound:
            self.left_sound = Audio(f'{sound_file_name}_left', volume=volume/2)

        self.right_sound = right_sound
        if not right_sound:
            self.right_sound = Audio(f'{sound_file_name}_right', volume=volume/2)
        # print('-------------------', self.left_sound, self.right_sound)
        self.loop = loop

        if autoplay:
            self.play()

        if auto_destroy:
            invoke(self.stop, destroy=True, delay=self.length)

        # print('aaaaaaaaaaaaa', volume)
        self.volume = volume
        self.balance = balance

    def balance_getter(self):
        return getattr(self, '_balance', 0)
    def balance_setter(self, value):
        self._balance = value
        self.volume = self.volume

    def volume_setter(self, value):
        self._volume = value
        pan = self.balance + .5
        print('-----------set volume to:', value, pan)
        self.right_sound.volume = lerp(0, .5, pan) * self._volume
        self.left_sound.volume = lerp(.5, 0, pan) * self._volume
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


if __name__ == '__main__':
    from ursina import *
    app = Ursina()

    a = Audio2('sine', loop=True, balance=-.5)
    pan_slider = Slider(min=-.5, max=.5, default=0, dynamic=True, setattr=(a,'balance'))

    app.run()
