from pydub import AudioSegment
from pydub.playback import play
from pathlib import Path
import glob

def create_panned_sounds(input_file):
    if input_file.suffix == '.ogg':
        audio = AudioSegment.from_ogg(input_file)
    elif input_file.suffix == '.wav':
        audio = AudioSegment.from_wav(input_file)
    else:
        raise ValueError("Input file must be in OGG or WAV format")

    audio = audio.set_channels(1)
    audio_left = audio.pan(-1)  # pan left
    audio_right = audio.pan(1)  # pan right

    audio_left.export(f'{input_file.parent / 'generated' / input_file.stem}_left.ogg', format='ogg')
    audio_right.export(f'{input_file.parent / 'generated' / input_file.stem}_right.ogg', format='ogg')
    print('done')

if __name__ == '__main__':
    # print('----', glob.escape('uoiowa_piano*.*'))
    # for file in Path('samples').glob(glob.escape('uoiowa_piano[n*].wav')):
    names = ('uoiowa_piano', 'uoiowa_guitar', 'drum')
    # pattern = pattern.replace('[','[[]').replace(']','[]]')
    for name in names:
        for file in Path('samples/').glob(f'{name}*.*'):
            if file.stem.endswith('_left') or file.stem.endswith('_right'):
                continue
            print('ddd', file)
            create_panned_sounds(file)
