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


def dynamics(str, duration=1, min=0, max=1):
    return 1

instruments = []
notes = 'zxcvbnmasdfghjklqwertyuiop1234567890'
class Instrument:
    def __init__(self, note_pattern, octave=0, speed=1, loops=1, dynamics=None, name='unititled'):
        if not dynamics:
            dynamics = [1,]
        self.note_pattern = note_pattern
        self.octave = octave
        self.speed = speed
        self.dynamics = dynamics
        self.loops = loops
        self.name = name
        instruments.append(self)

        self.notes = []
        self.is_chord = []
        self.durations = []
        for char in self.note_pattern:
            if char in notes:
                self.notes.append(notes.index(char))
                self.is_chord.append(char.isupper)
                self.durations.append(1)

            elif char == '-':
                self.durations[-1] += 1

            elif char == ' ':
                self.notes.append(None)
                self.is_chord.append(False)
                self.durations.append(1)

        print(self.notes, self.is_chord, self.durations)

from ursina import *
app = Ursina()

from ursina.prefabs.ursfx import ursfx
piano = Instrument('sfh---- wdf ', octave=-3, speed=4, loops=4)
piano = Instrument('hgfdgfds', octave=-3, speed=2, loops=4)

scale_changer.pattern = scale_changer.patterns['minor pentatonic']
scale_changer.scale_rotation = 4

for instrument in instruments:
    for loop in range(instrument.loops):
        cum_time = 0
        for (n, dur) in zip(instrument.notes, instrument.durations):
            print('--', n ,dur)
            if not n:
                continue

            delay = 1+( (cum_time + (loop * sum(instrument.durations))) /instrument.speed)
            duration = 1/8 * dur
            cum_time += dur

            chord = (0)


            for offset in (0,-2,2):
                n = scale_changer.note_offset(n) + (12*instrument.octave)
                a = Audio('sine.wav', loop=True, pitch=pow(1 / 1.05946309436, -n+offset), volume=1.0, autoplay=False)
                invoke(a.play, delay=delay)
                a.fade_out(delay=delay+duration, duration=.2)


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
