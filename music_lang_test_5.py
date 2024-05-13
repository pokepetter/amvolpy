from music_lang import *


import random
random.seed(3)
# possible_notes = 'asdfghjkl--'
# random_melody = ''.join([random.choice(possible_notes) for i in range(32)])
# print('aaaaaaaaaa', random_melody)
# rand = NoteSection(random_melody.upper(), octave=0, speed=1, loops=4, chord_delays=1/32, volume=.8, sus=1, attack=0)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, chord_delays=1/32, volume=.2, sus=1, attack=0, offset=2)
# #
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0, delay=.5)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), instrument='alternating_piano', octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2, delay=.4)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/32, volume=.125, sus=.5, attack=0, delay=.1)
# rand = NoteSection('lwwlwwkqqkqq'.upper(), octave=0, speed=2, loops=4, chord_delays=1/16, volume=.05, sus=.5, attack=0, offset=-2, delay=.2)
# rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2, delay=.3)

scale_changer.pattern = scale_changer.patterns['heptatonic']
scale_changer.base_note_offset = 6
# scale_changer.pattern = scale_changer.patterns['phrygian dominant']
# rand = NoteSection('R-R-R-R-RRR-R-R-R-RRE-E-E-E-E-EEE-E-E-E--EE--', speed=8, loops=4, chord_delays=.05, volume=.5, attack=.005, sus=.1, instrument='chip_square')
# rand = NoteSection('RYI--RYIRYI--RYIRYI--RYIRYI--RYIQET--QETQET--QETQET--QETQET--RYI', speed=8, loops=4, chord_delays=.0001, volume=.5, attack=.05, sus=.75, instrument='panned_piano')

# rand = NoteSection('RYI-RYI-RYI-RYI-RYI-RYI-RYI-RYI-QET-QET-QET-QET-QET-QET-QET-QET-', speed=6, loops=2, volume=.3, attack=.1, sus=.5, falloff=.3, chord_delays=.1, instrument='square')

rand = NoteSection('RYIRYIRYIRYIQETQETWRYETU', speed=2, loops=2, volume=.2, attack=.05, sus=.1, falloff=1, chord_delays=.1, instrument='square')
rand = NoteSection('I-ui-ui-oi-yu-yu-it-----', delay=1/16, speed=2, loops=4, chord_delays=.0, volume=.75, instrument='tagelharpa_pizz_horse_pulse')

rand = NoteSection('RYIRYIRYIRYIQETQETQETQET', speed=2, loops=4, chord_delays=.1, volume=.2, instrument='alternating_piano', delay=8*4)
application.time_scale = 55/60
render_note_sections()
import music_lang
app.run()
