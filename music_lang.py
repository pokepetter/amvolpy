from ursina import *
from audio2 import Audio2
from instrument_loader import load_instrument

app = Ursina(borderless=False)
window.exit_button.enabled = False

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

SYNTHS = dict()
note_sections = []
notes = 'zxcvbnmasdfghjklqwertyuiop1234567890'
uppercase_notes = 'ZXCVBNMASDFGHJKLQWERTYUIOP!"#¤%&/()='


class Synth:
    def __init__(self, name='default_synth', sample='uoiowa_piano', volume=.5, attack=0, sus=1, falloff=2, chord_shape=(0,-2,2), chord_delays=None, pan=-.05, spread=.05):
        # these are just default for new synth, you don't usually need them
        self.name = name
        self.sample = sample
        self.samples_and_pitches, attack, falloff, loop_samples = load_instrument(sample)
        self.volume = volume
        self.attack = attack
        self.sus = sus
        self.falloff = falloff
        self.pan = pan
        self.spread = spread
        self.octave = 0
        self.chord_shape = chord_shape
        self.chord_delays = chord_delays
        if chord_delays is None:
            self.chord_delays = [0 for e in chord_shape]
        elif isinstance(chord_delays, (float, int)):
            self.chord_delays = [i*chord_delays for i in range(len(chord_shape))]

        SYNTHS[name] = self


    def play_chord(self, n):
        for i, note_offset in enumerate(self.chord_shape):
            note_delay = self.chord_delays[i] * 1
            invoke(self.play, n+note_offset, delay=note_delay)


    def play(self, n, volume=None, attack=None, length=1, falloff=None, octave=0, pan=0, spread=.1):
        if volume is None: volume = self.volume
        if attack is None: attack = self.attack
        # if sus is None: sus = self.sus
        if falloff is None: falloff = self.falloff
        if octave is None: octave = self.octave
        if pan is None: pan = self.pan
        if spread is None: spread = self.spread

        n = scale_changer.note_offset(n) + (12*octave)
        sample, pitch = self.samples_and_pitches[n]
        print('-----------plat note', n, volume, attack, length, falloff)
        a = Audio2(sample, pitch=pitch, volume=0, autoplay=False, balance=pan, spread=spread)
        a.play()
        print('--------------------------------------', attack, length, falloff)
        a.animate('volume', volume, duration=attack, curve=curve.linear)
        a.animate('volume', 0, delay=length, duration=falloff, curve=curve.linear)
        # destroy(a, delay=length+falloff)


class AlternatingPiano(Synth):
    def play(self, n, volume=None, attack=None, length=1, falloff=None, octave=0, pan=0, spread=.1):
        # alternate side
        if not hasattr(self, 'i'):
            self.i = 0
        self.i += 1
        pan = (self.i % 2) -.5
        super().play(n=n, volume=volume, attack=attack, length=length, falloff=falloff, octave=octave, pan=pan, spread=spread)

class PannedPiano(Synth):
    def play(self, n, volume=None, attack=None, length=1, falloff=None, octave=0, pan=0, spread=None):
        # pan based on pitch
        pan = (n/24) -.75
        pan = clamp(pan, -.5, .5)
        # print('-----', pan)
        # print('-----ffffffff', self.falloff)
        super().play(n=n, volume=volume, attack=attack, length=length, falloff=falloff, octave=octave, pan=pan, spread=spread)

# default instrments
unique_instrument_names = set([path.stem.split('_n')[0] for path in Path('samples/').glob('*.*') if '_n' in path.stem])
default_synths = [PannedPiano(name=name, sample=name) for name in unique_instrument_names]

# custom instruments
piano = Synth(name='piano', sample='uoiowa_piano', falloff=.1)
panned_piano = PannedPiano(name='piano', sample='uoiowa_piano', falloff=.1)
my_violin = PannedPiano(name='my_violin', sample='violin', attack=0, falloff=.5)
# ambient_piano = Synth(name='ambient_piano', sample='uoiowa_piano', falloff=2)


class NoteSection:
    def __init__(self, note_pattern, octave=0, offset=0, chord_shape=(0,-2,2), chord_delays=None,
            volume=.5, speed=1, loops=1, dynamics=None, attack=None, note_length=1, falloff=None, pan=None, spread=None, time_scale=1, delay=0, name='unititled', instrument=panned_piano):

        if not dynamics:
            dynamics = [1,]

        if isinstance(instrument, str):
            instrument = SYNTHS[instrument]

        self.instrument = instrument
        self.note_pattern = note_pattern
        self.dynamics = dynamics
        self.loops = loops
        self.name = name
        self.speed = speed
        self.offset = offset
        self.time_scale = time_scale
        self.delay = delay
        self.chord_shape = chord_shape
        self.chord_delays = chord_delays

        # override instrument settings
        self.octave = octave
        self.attack = attack
        self.note_length = note_length
        self.falloff = falloff
        self.volume = volume
        self.pan = pan
        self.spread = spread

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



# real time note section
rtns = Empty(instrument=panned_piano, volume=.5, chord_shape=(0,), chord_delays=1/32, octave=0)


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

                attack = note_section.attack if note_section.attack is not None else note_section.instrument.attack
                # sus = note_section.sus if note_section.sus is not None else note_section.instrument.sus
                falloff = note_section.falloff if note_section.falloff is not None else note_section.instrument.falloff
                spread = note_section.spread if note_section.spread is not None else note_section.instrument.spread
                pan = note_section.pan if note_section.pan is not None else note_section.instrument.pan
                print('.-.............', attack, 'falloff', falloff, pan)

                invoke(note_section.instrument.play, n=note,
                    attack=attack/note_section.time_scale, length=note_section.note_length/note_section.time_scale, falloff=falloff/note_section.time_scale,
                    octave=note_section.octave, volume=note_section.volume,
                    # chord_shape=chord_shape, chord_delays=note_section.chord_delays,
                    delay=note_section.delay+(delay/note_section.time_scale), pan=pan, spread=spread)
                # invoke(play_note, note, instrument=note_section.instrument, attack=note_section.attack*note_section.time_scale, falloff=note_section.falloff*note_section.time_scale, octave=note_section.octave, volume=note_section.volume,
                #     chord_shape=chord_shape, chord_delays=note_section.chord_delays, sus=note_section.sus*note_section.time_scale, delay=note_section.delay+(delay*note_section.time_scale))



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

        # _oct = floor(n / 12)
        # _extra = n - (_oct*12)
        # print('play:', n, 'oct:', _oct, _extra)
        if held_keys['shift']:
            rtns.instrument.play_chord(n)
        rtns.instrument.play(n)


    if held_keys['control']:
        if key == '1':
            application.time_scale = 1
        elif key == '2':
            application.time_scale = .5

    if key == 'space':
        invoke(play_all, delay=.5)



from scale_changer_menu import ScaleChangerMenu
scale_changer_menu = ScaleChangerMenu()

instrument_picker = ButtonList({key : Func(setattr, rtns, 'instrument', value) for key, value in SYNTHS.items()})
# ursfx([(0.0, 1.0), (0.09, 0.5), (0.25, 0.5), (0.31, 0.5), (1.0, 0.0)], volume=1.0, wave='sine', pitch=-24, speed=2.2)
# class UrsfxSynth:

if __name__ == '__main__':
    # application.time_scale = 30/60
    # melody = NoteSection('adgjlkjg ', octave=-2, speed=4, loops=4)
    # melody = NoteSection('xvbmxvmxvmxvbmxvbmxvbmxvbmxvbmzcvnzcvnzcvnzcvnzcvnzcvnzcvnzcvn', octave=2, speed=9.25, loops=4, falloff=.25)
    # melody = NoteSection('HD', sample='sine', octave=2, speed=1, loops=4, attack=.5, falloff=.5, volume=.5, sus=.5, time_scale=4)
    scale_changer.pattern = scale_changer.patterns['phrygian dominant']
    melody = NoteSection('GDFSDAMS', octave=0, speed=1, loops=4, falloff=1/4, chord_delays=1/32, volume=.5, note_length=.75, attack=0)
    melody = NoteSection('HD', octave=2, speed=1, loops=4, attack=.5, falloff=.5, volume=.2, note_length=.5, time_scale=4)
    melody = NoteSection('qwertyuiop1234567654321poiuytrew', octave=-1, speed=8, loops=8, falloff=1/16, chord_delays=1/32, volume=.2, note_length=.2, attack=.025)

    random.seed(4)
    some_notes = 'GDFSDAMS ----'.lower()
    random_melody = ''.join([random.choice(some_notes) for i in range(32)])
    rand = NoteSection(random_melody, octave=2, speed=4, loops=1, falloff=1/8, chord_delays=1/32, volume=.4, note_length=.75, attack=.05, delay=8)

    random.seed(7)
    random_melody_2 = ''.join([random.choice(some_notes) for i in range(16)])
    rand_2 = NoteSection(random_melody_2, octave=3, speed=2, loops=1, falloff=1/4, chord_delays=1/32, volume=.4, note_length=.75, attack=.05, delay=16)
    # melody = NoteSection('GDFSDAMS', octave=0, speed=1, loops=4, falloff=1/2, chord_delays=1/32, volume=.1, instrument='noise')
    # melody = NoteSection('hgfdgfds'.upper(), octave=1, speed=2, loops=4, chord_delays=1/16, chord_shape=(0,2,4,6))
    # for e in note_sections:
    #     e.offset = -2
    # scale_changer.scale_rotation = 4
    app.run()
