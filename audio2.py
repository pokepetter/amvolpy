from ursina import *
from ursina.scripts.property_generator import generate_properties_for_class

@generate_properties_for_class()
class Audio2(Entity):
    def __init__(self, sound_file_name='', left_sound='', right_sound='', autoplay=True, auto_destroy=False,
        loop=False, volume=1, pitch=1, balance=0, spread=.1):
        super().__init__()
        self.left_sound = left_sound
        if not left_sound:
            self.left_sound = Audio(f'{sound_file_name}_left', volume=volume/2)
            if not self.left_sound.clip:
                self.left_sound.clip = sound_file_name

        self.right_sound = right_sound
        if not right_sound:
            self.right_sound = Audio(f'{sound_file_name}_right', volume=volume/2)
            if not self.right_sound.clip:
                self.right_sound.clip = sound_file_name
        # print('-------------------', self.left_sound, self.right_sound)
        self.loop = loop
        self.spread = spread
        self.phase_right = True
        self.alternate_phase = True

        if autoplay:
            self.play()

        if auto_destroy:
            invoke(self.stop, destroy=True, delay=self.length)

        self.pitch = pitch
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
        # print('-----------set volume to:', value, pan)
        self.right_sound.volume = lerp(0, .5, pan) * self._volume
        self.left_sound.volume = lerp(.5, 0, pan) * self._volume

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
        if self.balance <= 0:
            self.left_sound.play()
            invoke(self.right_sound.play, delay=self.spread)
        else:
            self.right_sound.play()
            invoke(self.left_sound.play, delay=self.spread)


    def fade_in(self, duration, volume=1):
        self.left_sound.animate('volume', volume, duration=duration)
        invoke(self.right_sound.animate, 'volume', volume, duration=duration, delay=self.spread)


    def fade_out(self, duration):
        self.left_sound.animate('volume', 0, duration=duration)
        invoke(self.right_sound.animate, 'volume', 0, duration=duration, delay=self.spread)



if __name__ == '__main__':
    app = Ursina(borderless=False)

    a = Audio2('uoiowa_piano_n36', loop=False, balance=-.5)
    pan_slider = Slider(min=-.5, max=.5, default=0, dynamic=True, setattr=(a,'balance'))
    spread_slider = Slider(min=0, max=1, default=0, dynamic=True, setattr=(a,'spread'), y=-.1)

    def spread():
        a.play()

    b = Button(scale=.1, y=.1, on_click=spread)

    app.run()
