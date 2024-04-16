from music_lang import *


import random
random.seed(3)
possible_notes = 'asdfghjkl--'
random_melody = ''.join([random.choice(possible_notes) for i in range(32)])
print('aaaaaaaaaa', random_melody)
rand = NoteSection(random_melody.upper(), octave=0, speed=1, loops=4, chord_delays=1/32, volume=.8, sus=1, attack=0)
rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, chord_delays=1/32, volume=.2, sus=1, attack=0, offset=2)
#
rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0, delay=.5)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), instrument='alternating_piano', octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2, delay=.4)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0, delay=.1)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2, delay=.2)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2, delay=.3)

scale_changer.pattern = scale_changer.patterns['minor pentatonic']
scale_changer.base_note_offset = 6
# scale_changer_menu.apply_preset(scale_changer_menu.presets['tony anderson - fields of green - hepta-6'])
rand = NoteSection('YRTE-RWEQ', octave=-1, speed=1, loops=4, chord_shape=(0,2,4,7,9,11,9,7,5,3,1,3,5,7,6,2), chord_delays=1/16, volume=.1, sus=1, attack=0, instrument='alternating_piano')

application.time_scale = 20/60
# NoteSection('werty-oiu-iuy---werty-oiu-i-y---', instrument='uoiowa_guitar', octave=1, speed=4, loops=4, chord_delays=0, volume=.3, sus=.5, attack=0, falloff=1/2)
# NoteSection('werty-oiu-iuy---werty-oiu-i-y---', instrument='uoiowa_guitar', octave=0, speed=4, loops=4, chord_delays=0, volume=.5, sus=.5, attack=0)
# NoteSection('g-gkg-gkf-fkf-fk', instrument='uoiowa_guitar', octave=0, speed=4, loops=8, chord_delays=0, volume=.3, sus=.1, attack=0, falloff=1/4)
# NoteSection('g-gkg-gkf-fkf-fk', octave=-1, speed=4, loops=32, chord_delays=0, volume=.3, sus=.1, attack=0, falloff=1/4, pan=-.1)
# NoteSection('xa', instrument='drum', octave=2, speed=2, loops=32, chord_delays=0, volume=.2, sus=1, attack=0, falloff=1/4, pan=-.3)
# NoteSection('ggg---jf--s-h-k-', instrument='drum', octave=1, speed=8, loops=32, chord_delays=0, volume=.1, sus=.3, attack=0, falloff=1/4)
# NoteSection('x---a---x-x-a---', instrument='drum', octave=0, speed=2, loops=32, chord_delays=0, volume=.3, sus=.2, attack=0, falloff=1/4)

# rand = NoteSection('ggg---jf--s-h-k--ga-fg sh', instrument='drum', octave=2, speed=8, loops=8, chord_delays=0, volume=.1, sus=.1, attack=0, falloff=1/4)
# rand = NoteSection(' x', instrument='drum', octave=2, speed=4, loops=8, chord_delays=0, volume=.3, sus=.1, attack=0, falloff=1/4)
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
    # music_lang.input(key)
    if key == 'space':
        invoke(play_all, delay=.5)
app.run()
