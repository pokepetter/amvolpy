
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





piano = Instrument('GDFSDAMS', octave=0, speed=2, loops=4, fade=.5, offset=0, chord_delays=1/32, volume=.5)
piano = Instrument('GDFSDAMS', octave=0, speed=2, loops=4, fade=.5, offset=0, chord_delays=1/32, volume=.1, sample='noise')

PIANO
§ |sfh wdf |
-4oct o0 s3 l4
\ .5
~ |__..--^^--..__| (.5, .9)
% -.5


'''
