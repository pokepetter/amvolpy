from music_lang import *



possible_notes = 'asdfghjkl'
random_melody = ''.join([random.choice(possible_notes) for i in range(32)])
print('aaaaaaaaaa', random_melody)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.5, sus=1, attack=0)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

scale_changer.pattern = scale_changer.patterns['phrygian dominant']
application.time_scale = 45/60
NoteSection('werty-oiu-iuy---werty-oiu-i-y---', instrument='uoiowa_guitar', octave=1, speed=4, loops=4, chord_delays=0, volume=.3, sus=.5, attack=0, fade=1/2)
NoteSection('werty-oiu-iuy---werty-oiu-i-y---', instrument='uoiowa_guitar', octave=0, speed=4, loops=4, chord_delays=0, volume=.5, sus=.5, attack=0)
NoteSection('g-gkg-gkf-fkf-fk', instrument='uoiowa_guitar', octave=0, speed=4, loops=8, chord_delays=0, volume=.3, sus=.1, attack=0, fade=1/4)
NoteSection('g-gkg-gkf-fkf-fk', octave=-1, speed=4, loops=32, chord_delays=0, volume=.3, sus=.1, attack=0, fade=1/4)
NoteSection('xa', instrument='drum', octave=0, speed=2, loops=32, chord_delays=0, volume=.3, sus=.2, attack=0, fade=1/4)
NoteSection('ggg---jf--s-h-k-', instrument='drum', octave=2, speed=8, loops=32, chord_delays=0, volume=.1, sus=.1, attack=0, fade=1/4)
NoteSection('x---a---x-x-a---', instrument='drum', octave=0, speed=2, loops=32, chord_delays=0, volume=.3, sus=.2, attack=0, fade=1/4)

# rand = NoteSection('ggg---jf--s-h-k--ga-fg sh', instrument='drum', octave=2, speed=8, loops=8, chord_delays=0, volume=.1, sus=.1, attack=0, fade=1/4)
# rand = NoteSection(' x', instrument='drum', octave=2, speed=4, loops=8, chord_delays=0, volume=.3, sus=.1, attack=0, fade=1/4)
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
