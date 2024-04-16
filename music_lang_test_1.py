from music_lang import *


scale_changer.pattern = scale_changer.patterns['hexadiatonic']

possible_notes = 'asdfghjkl'
random_melody = ''.join([random.choice(possible_notes) for i in range(32)])
print('aaaaaaaaaa', random_melody)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.5, sus=1, attack=0)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

application.time_scale = 45/60
rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
rand = NoteSection('64534231'.upper(), octave=0, speed=1/3*2, loops=4, chord_delays=1/16, volume=.5, sus=1, attack=0, instrument=piano, pan=-.1)

sine_instr = PannedPiano(name='sine', sample='sine')

# rand = NoteSection('12', instrument=sine_instr, octave=0, time_scale=2, loops=4, chord_delays=1/16, volume=.5, attack=.5, falloff=.5)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

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
