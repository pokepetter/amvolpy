from ursina import *
app = Ursina()

import scale_changer

# pattern = § |sfh wdf |


# PIANO
# § |sfh wdf | -4O -2 X3
# ~ |__..--^^--..__| _=.5,
# % -.5
#
# PIANO_2
# § pattern -2O X1/4
# ~ |__..--^^--..__| _=.5,
# % -.5


# dynamics = dynamics('__..--^^--..__', duration=1, min=.5, max=1)
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



def dynamics(str, duration=1, min=0, max=1):
    return 1

BPM = 60

instruments = []
notes = 'zxcvbnmasdfghjklqwertyuiop1234567890'
class Instrument:
    def __init__(self, note_pattern, octave=0, offset=0, chord_shape=(0,-2,2), chord_delays=None,
            volume=.5, speed=1, loops=1, dynamics=None, sus=0, fade=.2, name='unititled', sample='square_440hz',
            ):

        if not dynamics:
            dynamics = [1,]
        self.sample = sample
        self.note_pattern = note_pattern
        self.octave = octave
        self.speed = speed
        self.dynamics = dynamics
        self.loops = loops
        self.name = name
        self.sus = sus
        self.fade = fade
        self.offset = offset
        self.volume = volume

        self.chord_shape = chord_shape
        self.chord_delays = chord_delays
        instruments.append(self)

        self.notes = []
        self.is_chord = []

        self.durations = []
        for char in self.note_pattern:
            if char.lower() in notes:
                self.notes.append(notes.index(char.lower()))
                self.is_chord.append(char.isupper())
                self.durations.append(1)

            elif char == '-':
                self.durations[-1] += 1

            elif char == ' ':
                self.notes.append(None)
                self.is_chord.append(False)
                self.durations.append(1)

        print(self.notes, 'ischord:', self.is_chord, self.durations)



def play_note(note, sample='square_440hz', volume=1, sus=0, falloff=1/2, chord=(0,), chord_delays=None, octave=0):
    print('note in:', note, 'chord:', chord)
    if chord_delays is None:
        chord_delays = [0 for e in chord]
    elif isinstance(chord_delays, (float, int)):
        chord_delays = [i*chord_delays for i in range(len(chord))]


    for i, chord_offset in enumerate(chord):
        n = note + chord_offset
        print('play note:', n, chord_offset)
        n = scale_changer.note_offset(n) + (12*octave)
        # a = Audio2('sine', loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume)
        a = Audio(sample, loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume, autoplay=False)
        note_delay = chord_delays[i] * 1
        invoke(a.play, delay=note_delay)
        print('sus', note_delay+sus)
        a.fade_out(duration=falloff, delay=note_delay+sus)


# application.time.scale =
def play_all():
    for i, instrument in enumerate(instruments):
        for loop in range(instrument.loops):
            cum_time = 0
            for (note, dur) in zip(instrument.notes, instrument.durations):
                # print('--', n ,dur)
                if not note:
                    continue

                delay = (1+( (cum_time + (loop * sum(instrument.durations))) /instrument.speed))
                duration = 1/8 * dur
                cum_time += dur

                chord = (0, )
                if instrument.is_chord[i]:
                    chord = instrument.chord_shape
                # Text(text='', )

                balance = ((cum_time%2)-.5)*2

                note += instrument.offset
                invoke(play_note, note, sample=instrument.sample, falloff=instrument.fade, octave=instrument.octave, volume=instrument.volume,
                    chord=chord, chord_delays=instrument.chord_delays, sus=instrument.sus, delay=delay)



def input(key):
    if not held_keys['control'] and key in notes:
        n = notes.index(key)
        # n = scale_changer.note_offset(n)
        chord = (0,)
        if held_keys['shift']:
            chord = (0,-2,2)

        play_note(n, chord=chord, chord_delays=0, sample='square_440hz', sus=1/4, volume=.5)

    if held_keys['control']:
        if key == '1':
            application.time_scale = 1
        elif key == '2':
            application.time_scale = .5

application.time_scale = 1
# piano = Instrument('adgjlkjg ', octave=-2, speed=4, loops=4)
# piano = Instrument('xvbmxvmxvmxvbmxvbmxvbmxvbmxvbmzcvnzcvnzcvnzcvnzcvnzcvnzcvnzcvn', octave=2, speed=9.25, loops=4, fade=.25, offset=-0)
piano = Instrument('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/4, offset=-0, chord_delays=1/32, volume=.5, sus=3/4)
# piano = Instrument('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/2, offset=-0, chord_delays=1/32, volume=.1, sample='noise')
# piano = Instrument('hgfdgfds'.upper(), octave=1, speed=2, loops=4, chord_delays=1/16, chord_shape=(0,2,4,6))

scale_changer.pattern = scale_changer.patterns['hexadiatonic']
# scale_changer.scale_rotation = 4

play_all()

app.run()
