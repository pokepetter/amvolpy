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

instruments = []
notes = 'zxcvbnmasdfghjklqwertyuiop1234567890'
class Instrument:
    def __init__(self, note_pattern, octave=0, offset=0, speed=1, loops=1, dynamics=None, fade=.2, name='unititled'):
        if not dynamics:
            dynamics = [1,]
        self.note_pattern = note_pattern
        self.octave = octave
        self.speed = speed
        self.dynamics = dynamics
        self.loops = loops
        self.name = name
        self.fade = fade
        self.offset = offset
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



def play_note(note, instrument='sine', volume=1, falloff=.5, chord=(0,), octave=0):
    print('note in:', note, 'chord:', chord)
    for chord_offset in chord:
        n = note + chord_offset
        print('play note:', n, chord_offset)
        n = scale_changer.note_offset(n) + (12*octave)
        a = Audio2('sine', loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume)
        a.fade_out(duration=falloff)


from ursina.prefabs.ursfx import ursfx
# piano = Instrument('adgjlkjg ', octave=-2, speed=4, loops=4)
# piano = Instrument('xvbmxvmxvmxvbmxvbmxvbmxvbmxvbmzcvnzcvnzcvnzcvnzcvnzcvnzcvnzcvn', octave=2, speed=9.25, loops=4, fade=.25, offset=-0)
piano = Instrument('GDFSDAMS', octave=0, speed=2, loops=4, fade=.5, offset=-0)
# piano = Instrument('hgfdgfds', octave=-3, speed=2, loops=4)

scale_changer.pattern = scale_changer.patterns['hexadiatonic']
BPM = 140
# scale_changer.scale_rotation = 4

for i, instrument in enumerate(instruments):
    for loop in range(instrument.loops):
        cum_time = 0
        for (note, dur) in zip(instrument.notes, instrument.durations):
            # print('--', n ,dur)
            if not note:
                continue

            delay = (1+( (cum_time + (loop * sum(instrument.durations))) /instrument.speed)) * 1
            duration = 1/8 * dur
            cum_time += dur

            chord = (0, )
            if instrument.is_chord[i]:
                chord = (0,-2,2)
            # Text(text='', )

            balance = ((cum_time%2)-.5)*2

            note += instrument.offset
            invoke(play_note, note, falloff=instrument.fade, octave=instrument.octave, chord=chord, delay=delay)



def input(key):
    if key in notes:
        n = notes.index(key)
        # n = scale_changer.note_offset(n)
        chord = (0,)
        if held_keys['shift']:
            chord = (0,-2,2)

        play_note(n, chord=chord)

app.run()

'''
sclang
FoxDot.start
0.exit
'''

'''
name: across destiny

drums:
    delay:
    speed:---
    scale:pentatonic
    melody = '1---2- 3---4-'
    after 3 loops: speed += 1
        after 1: fade_speed(speed-1)
    after 8 loops: fade_out(duration=2 loops)
    every 2 loop:
        play drums_2 for 1 loop


drums_2:
    pattern= "_^*^_^*^_^*^"
    dynamic: pattern='__..--^^--..__', duration=1L, range(.5,1)

main_melody:
    # delay: drums_2.end
    "etuopout"-3O

pattern = § |sfh wdf |


PIANO
§ |sfh wdf | -4O -2 X3
~ |__..--^^--..__| _=.5,
% -.5

PIANO_2
§ pattern -2O X1/4
~ |__..--^^--..__| _=.5,
% -.5

BASS
§ |[adg][sfh]| -5o x1/8


'rtyuiuyt'
'w---wry-, y---yri-, e----etu-, y-y-yte-'
layout:

fadein:        |---..__
main melody:   |    ------------....____    _.--------
drums:         |-------------------------------    -----------------    |
bass:          |--------------------.__.-^^^-
'''
