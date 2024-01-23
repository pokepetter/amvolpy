from ursina import *
app = Ursina(borderless=False, size=Vec2(1920,1080))

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
    def __init__(self, note_pattern, octave=0, offset=0, chord_shape=(0,-2,2), chord_delays=None,
            volume=.5, speed=1, loops=1, dynamics=None, attack=0, sus=0, fade=.2, time_scale=1, delay=0, name='unititled', sample='square_440hz',
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
        self.attack = attack
        self.sus = sus
        self.fade = fade
        self.offset = offset
        self.volume = volume
        self.time_scale = time_scale
        self.delay = delay

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



def play_note(note, sample='square_440hz', volume=1, attack=0, sus=0, falloff=1/2, chord=(0,), chord_delays=None, octave=0):
    # print('note in:', note, 'chord:', chord)
    if chord_delays is None:
        chord_delays = [0 for e in chord]
    elif isinstance(chord_delays, (float, int)):
        chord_delays = [i*chord_delays for i in range(len(chord))]


    for i, chord_offset in enumerate(chord):
        n = note + chord_offset
        # print('play note:', n, chord_offset)
        n = scale_changer.note_offset(n) + (12*octave)
        # a = Audio2('sine', loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume)
        a = Audio(sample, loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume, autoplay=False)
        note_delay = chord_delays[i] * 1

        invoke(a.play, delay=note_delay)
        a.volume = 0
        a.animate('volume', volume, duration=attack, curve=curve.linear)
        # print('volume', a.volume, attack, 'sus:', sus, 'delay:', note_delay+sus)
        a.animate('volume', 0, duration=falloff, delay=note_delay+sus, curve=curve.linear)
        destroy(a, delay=note_delay+sus+falloff)


# application.time.scale =
def play_all():
    for i, instrument in enumerate(instruments):
        for loop in range(instrument.loops):
            cum_time = 0
            for j, (note, dur) in enumerate(zip(instrument.notes, instrument.durations)):
                # print('--', note, dur)
                if not note:
                    continue

                delay = (( (cum_time + (loop * sum(instrument.durations))) /instrument.speed))
                duration = 1/8 * dur
                cum_time += dur

                chord = (0, )
                if instrument.is_chord[j]:
                    chord = instrument.chord_shape
                # Text(text='', )

                balance = ((cum_time%2)-.5)*2

                note += instrument.offset
                invoke(play_note, note, sample=instrument.sample, attack=instrument.attack*instrument.time_scale, falloff=instrument.fade*instrument.time_scale, octave=instrument.octave, volume=instrument.volume,
                    chord=chord, chord_delays=instrument.chord_delays, sus=instrument.sus*instrument.time_scale, delay=instrument.delay+(delay*instrument.time_scale))



def input(key):
    if not held_keys['control'] and key in notes:
        n = notes.index(key)
        # n = scale_changer.note_offset(n)
        chord = (0,)
        if held_keys['shift']:
            chord = (0,-2,2)
            # chord = (0,1,2,4,5,7)

        print('play:', n)
        if held_keys['shift']:
            chord = (0,-2,2)
            play_note(n, chord=chord, sus=1/4, volume=.5, chord_delays=1/32)
            play_note(n-2, chord=chord, sus=1/4, volume=.2, chord_delays=1/16)
        else:
            play_note(n, chord=chord, chord_delays=1/16, sus=1/16, volume=.5)
        # rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

        # rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.5, sus=1, attack=0)
        # rand = Instrument(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

    if held_keys['control']:
        if key == '1':
            application.time_scale = 1
        elif key == '2':
            application.time_scale = .5

    if key == 'space':
        invoke(play_all, delay=.5)




# window.position=(0,0)
# window.size = Vec2(1920,1080)

# window.color = color.hex('#282c34')
# Text.default_font = 'VeraMono.ttf'
# text_editor = TextField(register_mouse_input=True, line_height=1.3, x=-.25, y=.25, active=False, ignore=True)
# text_editor.line_numbers.enabled=True
# text_editor.bg.color = window.color
#
# text_editor.text_entity.text_colors['default'] = color.hex('#abb2bf')
# text_editor.text_entity.text_colors['cyan'] = color.hex('#61afef')
# text_editor.text_entity.text_colors['purple'] = color.hex('#c678dd')
# text_editor.text_entity.text_colors['orange'] = color.hex('#d19a66')
# text_editor.text_entity.text_colors['string_color'] = color.hex('#98c379')
# text_editor.text_entity.text_colors['red'] = color.hex('#e06c75')
# text_editor.text_entity.text_colors['gray'] = color.hex('#5c6370')
# text_editor.line_numbers.color = lerp(color.hex('#5c6370'), window.color, .5)
#
# for e in range(10):
#     text_editor.replacements[f' {e}'] = f' ☾orange☽{e}' # numbers
#     text_editor.replacements[f'={e}'] = f'=☾orange☽{e}' # numbers
#     text_editor.replacements[f'.{e}'] = f'☾orange☽.{e}' # numbers
#     text_editor.replacements[f'-{e}'] = f'☾orange☽-{e}' # numbers
#     text_editor.replacements[f'({e}'] = f'(☾orange☽{e}' # numbers
#
#
# text_editor.replacements.update({
#     **{f'{e}': f'☾cyan☽{e}' for e in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'},
#
#     'from ':    f'☾purple☽from ☾default☽',
#     'import ':  f'☾purple☽import ☾default☽',
#     'def ':     f'☾purple☽def ☾default☽',
#     'for ':     f'☾purple☽for ☾default☽',
#     'if ':      f'☾purple☽if ☾default☽',
#     'with ':    f'☾purple☽with ☾default☽',
#     ' in ':     f'☾purple☽ in ☾default☽',
#
#     '\',':    f'\'☾default☽,',   # end quote
#     '\':':    f'\':☾default☽',   # end quote
#     '\')':    f'\')☾default☽',   # end quote
#     '\']':    f'\'☾default☽]',   # end quote
#     ' \'':    f' ☾string_color☽\'', # start quote
#     '=\'':    f'=☾string_color☽\'', # start quote
#     '(\'':    f'(☾string_color☽\'', # start quote
#     '[\'':    f'[☾string_color☽\'', # start quote
#
#     '=':        f'☾purple☽=☾default☽',
#     '+':        f'☾purple☽+☾default☽',
#     '-':        f'☾purple☽-☾default☽',
#     '*':        f'☾purple☽*☾default☽',
#
#     'print(':   f'☾func_color☽print☾default☽(',
#     'range(':   f'☾func_color☽range☾default☽(',
#     '__init__': f'☾func_color☽__init__☾default☽',
#     'super':    f'☾func_color☽super☾default☽',
#
#     'update(':   f'☾cyan☽update☾default☽(',
#     'input(':    f'☾cyan☽input☾default☽(',
#
#     'class ':   f'☾class_color☽class ☾default☽',
#     'self.':    f'☾class_color☽self☾default☽.',
#     '(self)':   f'(☾class_color☽self☾default☽)',
#     'self,':    f'☾class_color☽self☾default☽,',
#
#     '.':    f'.☾red☽',
#     ' ':    f' ☾default☽',
#     '(':    f'☾default☽(',
#     ')':    f'☾default☽)',
#     ', ':    f'☾default☽, ',
#     })
# text_editor.text = '''scale_changer.pattern = scale_changer.patterns['hexadiatonic']
# piano = Instrument('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/4, offset=-0, chord_delays=1/32, volume=.5, sus=.75, attack=0)
# piano = Instrument('HD', sample='noise', octave=2, speed=1, loops=4, attack=.5, fade=.5, offset=-0, volume=.2, sus=.5, time_scale=4)
# piano = Instrument('qwertyuiop1234567654321poiuytrew', octave=-1, speed=8, loops=8, fade=1/16, offset=-0, chord_delays=1/32, volume=.2, sus=.2, attack=.025)
#
# random.seed(4)
# notes = 'GDFSDAMS ----'.lower()
# random_melody = ''.join([random.choice(notes) for i in range(32)])
# rand = Instrument(random_melody, octave=2, speed=4, loops=1, fade=1/8, offset=-0, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=8)
#
# random.seed(7)
# random_melody_2 = ''.join([random.choice(notes) for i in range(16)])
# rand_2 = Instrument(random_melody_2, octave=3, speed=2, loops=1, fade=1/4, offset=-0, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=16)
# '''
# text_editor.render()
# text_editor.x=-.7
# text_editor.scale = .65


if __name__ == '__main__':
    # application.time_scale = 30/60
    # piano = Instrument('adgjlkjg ', octave=-2, speed=4, loops=4)
    # piano = Instrument('xvbmxvmxvmxvbmxvbmxvbmxvbmxvbmzcvnzcvnzcvnzcvnzcvnzcvnzcvnzcvn', octave=2, speed=9.25, loops=4, fade=.25)
    # piano = Instrument('HD', sample='sine', octave=2, speed=1, loops=4, attack=.5, fade=.5, volume=.5, sus=.5, time_scale=4)
    scale_changer.pattern = scale_changer.patterns['hexadiatonic']
    piano = Instrument('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/4, chord_delays=1/32, volume=.5, sus=.75, attack=0)
    piano = Instrument('HD', sample='noise', octave=2, speed=1, loops=4, attack=.5, fade=.5, volume=.2, sus=.5, time_scale=4)
    piano = Instrument('qwertyuiop1234567654321poiuytrew', octave=-1, speed=8, loops=8, fade=1/16, chord_delays=1/32, volume=.2, sus=.2, attack=.025)

    random.seed(4)
    some_notes = 'GDFSDAMS ----'.lower()
    random_melody = ''.join([random.choice(some_notes) for i in range(32)])
    rand = Instrument(random_melody, octave=2, speed=4, loops=1, fade=1/8, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=8)

    random.seed(7)
    random_melody_2 = ''.join([random.choice(some_notes) for i in range(16)])
    rand_2 = Instrument(random_melody_2, octave=3, speed=2, loops=1, fade=1/4, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=16)
    # piano = Instrument('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/2, chord_delays=1/32, volume=.1, sample='noise')
    # piano = Instrument('hgfdgfds'.upper(), octave=1, speed=2, loops=4, chord_delays=1/16, chord_shape=(0,2,4,6))
    # for e in instruments:
    #     e.offset = -2

    # scale_changer.scale_rotation = 4
    app.run()
