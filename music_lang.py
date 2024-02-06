from ursina import *
app = Ursina(borderless=False)

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

note_sections = []
notes = 'zxcvbnmasdfghjklqwertyuiop1234567890'
uppercase_notes = 'ZXCVBNMASDFGHJKLQWERTYUIOP!"#¤%&/()='

class NoteSection:
    def __init__(self, note_pattern, octave=0, offset=0, chord_shape=(0,-2,2), chord_delays=None,
            volume=.5, speed=1, loops=1, dynamics=None, attack=0, sus=0, fade=.2, time_scale=1, delay=0, name='unititled', instrument='uoiowa_piano',
            ):

        if not dynamics:
            dynamics = [1,]
        self.instrument = instrument
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
        note_sections.append(self)

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

from instrument_loader import load_instrument

instruments = dict()
for instr in ('uoiowa_piano', 'uoiowa_guitar', 'sine', 'drum', 'noise'):
    samples_and_pitches, attack, falloff, loop_samples = load_instrument(instr)
    instruments[instr] = samples_and_pitches
# samples_and_pitches, attack, falloff, loop_samples = load_note_section('uoiowa_guitar')
# self.sounds = [Audio(e[0], loop=self.loop_samples, pitch=e[1], volume=0, is_playing=False) for e in self.samples_and_pitches]
# samples, attack, falloff, loop_samples = load_note_section('uoiowa_piano')
# for e in samples_and_pitches:
#     print(e[0], 'pitch:', e[1])
SYNTHS = []


class Synth:
    def __init__(self, name='default_synth', sample='uoiowa_piano', volume=.5, attack=0, sus=0, falloff=1/2, chord_shape=(0,-2,2), chord_delays=None, pan=0):
        # these are just default for new synth, you don't usually need them
        self.sample = sample
        self.samples_and_pitches, attack, falloff, loop_samples = load_instrument(sample)
        self.volume = volume
        self.attack = attack
        self.sus = sus
        self.falloff = falloff
        self.pan = pan
        self.chord_shape = chord_shape
        self.chord_delays = chord_delays
        if chord_delays is None:
            self.chord_delays = [0 for e in chord_shape]
        elif isinstance(chord_delays, (float, int)):
            self.chord_delays = [i*chord_delays for i in range(len(chord_shape))]

        SYNTHS.append(self)

    def play(self, n, sample=Default, volume=Default, attack=Default, sus=Default, falloff=Default, octave=0):
        if sample == Default:   sample = self.sample
        if volume == Default:   volume = self.volume
        if attack == Default:   attack = self.attack
        if sus ==    Default:   sus = self.sus
        if falloff ==Default:   falloff = self.falloff

        n = scale_changer.note_offset(n) + (12*octave)
        sample, pitch = self.samples_and_pitches[n]
        a = Audio(sample, pitch=pitch, volume=0, autoplay=False)
        print('-----------', sample, pitch, volume, a)
        a.play()
        a.animate('volume', volume, duration=attack, curve=curve.linear)
        # a.animate('volume', 0, duration=falloff, delay=sus, curve=curve.linear)
        # destroy(a, delay=sus+falloff)

    def play_chord(self, n):
        for i, note_offset in enumerate(self.chord_shape):
            note_delay = self.chord_delays[i] * 1
            invoke(self.play, n+note_offset, delay=note_delay)

piano = Synth('piano', sample='uoiowa_piano')
ambient_piano = Synth('ambient_piano', sample='uoiowa_piano', falloff=2)


def play_note(note, instrument='uoiowa_piano', volume=1, attack=0, sus=0, falloff=1/2, chord_shape=(0,), chord_delays=None, octave=0, pan=0):
    # print('note in:', note, 'chord:', chord)
    if chord_delays is None:
        chord_delays = [0 for e in chord_shape]
    elif isinstance(chord_delays, (float, int)):
        chord_delays = [i*chord_delays for i in range(len(chord_shape))]


    for i, note_offset in enumerate(chord_shape):
        n = note + note_offset
        # print('play note:', n, chord_shape)
        n = scale_changer.note_offset(n) + (12*octave)
        # a = Audio2('sine', loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume)
        # a = Audio(sample, loop=True, pitch=pow(1 / 1.05946309436, -n+24), volume=volume, autoplay=False)
        # print('play note:', n, 'len samples:', (len(samples)))
        sample, pitch = instruments[instrument][n]
        a = Audio(sample, pitch=pitch, volume=1)
        note_delay = chord_delays[i] * 1

        invoke(a.play, delay=note_delay)
        a.volume = 0
        a.animate('volume', volume, duration=attack, curve=curve.linear)
        # print('volume', a.volume, attack, 'sus:', sus, 'delay:', note_delay+sus)
        a.animate('volume', 0, duration=falloff, delay=note_delay+sus, curve=curve.linear)
        destroy(a, delay=note_delay+sus+falloff)


# application.time.scale =
def play_all():
    for i, note_section in enumerate(note_sections):
        for loop in range(note_section.loops):
            cum_time = 0
            for j, (note, dur) in enumerate(zip(note_section.notes, note_section.durations)):
                # print('--', note, dur)
                if not note:
                    continue

                delay = (( (cum_time + (loop * sum(note_section.durations))) /note_section.speed))
                duration = 1/8 * dur
                cum_time += dur

                chord_shape = (0, )
                if note_section.is_chord[j]:
                    chord_shape = note_section.chord_shape
                # Text(text='', )

                balance = ((cum_time%2)-.5)*2

                note += note_section.offset
                invoke(play_note, note, instrument=note_section.instrument, attack=note_section.attack*note_section.time_scale, falloff=note_section.fade*note_section.time_scale, octave=note_section.octave, volume=note_section.volume,
                    chord_shape=chord, chord_delays=note_section.chord_delays, sus=note_section.sus*note_section.time_scale, delay=note_section.delay+(delay*note_section.time_scale))


# real time note section
rtns = Empty(instrument='uoiowa_piano', volume=.5, attack=0, sus=1/16, falloff=1, chord_shape=(0,), chord_delays=1/32, octave=0)

def input(key):
    if not held_keys['control'] and key in notes or key in ',.-':
        if key not in ',.-':
            n = notes.index(key)
        else:
            print('random')
            # if key == ',':  n = notes.index(random.choice('zxcvbnm'))
            if key == ',':  random_key = random.choice('asdfghjkl')
            if key == '.':  random_key = random.choice('qwertyuiop')
            if key == '-':  random_key = random.choice('1234567890')
            print_on_screen(random_key)
            n = notes.index(random_key)
        # n = scale_changer.note_offset(n)
        chord_shape = (0,)
        if held_keys['shift']:
            chord_shape = (0,-2,2)
            # chord = (0,1,2,4,5,7)

        _oct = floor(n / 12)
        _extra = n - (_oct*12)
        print('play:', n, 'oct:', _oct, _extra)
        if held_keys['shift']:
            piano.play_chord(n)
            # chord_shape = (0,-2,2)
            # play_note(n, chord=chord, sus=1/4, volume=.5, falloff=1, chord_delays=1/32)
            # play_note(n-2, chord=chord, sus=1/4, volume=.2, chord_delays=1/16)    # extra harmony
        # else:
        # play_note(n, instrument=rtns.instrument, chord_shape=chord_shape, volume=rtns.volume, attack=rtns.attack, sus=rtns.sus, falloff=rtns.falloff, chord_delays=rtns.chord_delays, octave=rtns.octave)
        piano.play(n)
        # rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)

        # rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.5, sus=1, attack=0)
        # rand = NoteSection(random_melody.upper(), octave=1, speed=1, loops=4, fade=1/16, chord_delays=1/32, volume=.05, sus=1, attack=0, offset=2)


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
# piano = NoteSection('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/4, offset=-0, chord_delays=1/32, volume=.5, sus=.75, attack=0)
# piano = NoteSection('HD', sample='noise', octave=2, speed=1, loops=4, attack=.5, fade=.5, offset=-0, volume=.2, sus=.5, time_scale=4)
# piano = NoteSection('qwertyuiop1234567654321poiuytrew', octave=-1, speed=8, loops=8, fade=1/16, offset=-0, chord_delays=1/32, volume=.2, sus=.2, attack=.025)
#
# random.seed(4)
# notes = 'GDFSDAMS ----'.lower()
# random_melody = ''.join([random.choice(notes) for i in range(32)])
# rand = NoteSection(random_melody, octave=2, speed=4, loops=1, fade=1/8, offset=-0, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=8)
#
# random.seed(7)
# random_melody_2 = ''.join([random.choice(notes) for i in range(16)])
# rand_2 = NoteSection(random_melody_2, octave=3, speed=2, loops=1, fade=1/4, offset=-0, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=16)
# '''
# text_editor.render()
# text_editor.x=-.7
# text_editor.scale = .65
from scale_changer_menu import ScaleChangerMenu
scale_changer_menu = ScaleChangerMenu()

instrument_picker = ButtonList({key : Func(setattr, rtns, 'instrument', key) for key in instruments.keys()})
# ursfx([(0.0, 1.0), (0.09, 0.5), (0.25, 0.5), (0.31, 0.5), (1.0, 0.0)], volume=1.0, wave='sine', pitch=-24, speed=2.2)
# class UrsfxSynth:

if __name__ == '__main__':
    # application.time_scale = 30/60
    # melody = NoteSection('adgjlkjg ', octave=-2, speed=4, loops=4)
    # melody = NoteSection('xvbmxvmxvmxvbmxvbmxvbmxvbmxvbmzcvnzcvnzcvnzcvnzcvnzcvnzcvnzcvn', octave=2, speed=9.25, loops=4, fade=.25)
    # melody = NoteSection('HD', sample='sine', octave=2, speed=1, loops=4, attack=.5, fade=.5, volume=.5, sus=.5, time_scale=4)
    scale_changer.pattern = scale_changer.patterns['phrygian dominant']
    melody = NoteSection('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/4, chord_delays=1/32, volume=.5, sus=.75, attack=0)
    melody = NoteSection('HD', octave=2, speed=1, loops=4, attack=.5, fade=.5, volume=.2, sus=.5, time_scale=4)
    melody = NoteSection('qwertyuiop1234567654321poiuytrew', octave=-1, speed=8, loops=8, fade=1/16, chord_delays=1/32, volume=.2, sus=.2, attack=.025)

    random.seed(4)
    some_notes = 'GDFSDAMS ----'.lower()
    random_melody = ''.join([random.choice(some_notes) for i in range(32)])
    rand = NoteSection(random_melody, octave=2, speed=4, loops=1, fade=1/8, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=8)

    random.seed(7)
    random_melody_2 = ''.join([random.choice(some_notes) for i in range(16)])
    rand_2 = NoteSection(random_melody_2, octave=3, speed=2, loops=1, fade=1/4, chord_delays=1/32, volume=.4, sus=.75, attack=.05, delay=16)
    # melody = NoteSection('GDFSDAMS', octave=0, speed=1, loops=4, fade=1/2, chord_delays=1/32, volume=.1, instrument='noise')
    # melody = NoteSection('hgfdgfds'.upper(), octave=1, speed=2, loops=4, chord_delays=1/16, chord_shape=(0,2,4,6))
    # for e in note_sections:
    #     e.offset = -2


    # scale_changer.scale_rotation = 4
    app.run()
