from music_lang import *


scale_changer.pattern = scale_changer.patterns['hexadiatonic']

possible_notes = 'asdfghjkl'
random_melody = ''.join([random.choice(possible_notes) for i in range(32)])
print('aaaaaaaaaa', random_melody)
# rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.5, sus=1, attack=0)
# rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

application.time_scale = 45/60
# rand = Instrument('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
# rand = Instrument('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
rand = Instrument('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
rand = Instrument('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
# rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

# gda(h?)e
# e dur
#
# under:
# 'a(h) - d - e - f# - a(h)'
#
#
# troll: a e a+ c#
# (h) c# e f# a
import music_lang
def input(key):
    music_lang.input(key)
    if key == 'space':
        invoke(play_all, delay=.5)
app.run()
