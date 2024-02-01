import glob
from ursina import application


def get_tags(string, start_tag, end_tag):
    tags = list()

    for s in string.split(start_tag)[1:]:
        # print(s.split(end_tag)[0])
        tags.append(s.split(end_tag)[0])

    return tags

# get_tags('names_nsma[ejgaogj]fjio[rijg][gjk3][9]', '[', ']')

def load_instrument(name):
    samples = [None, ] * 128
    attack, falloff, loop_samples = .05, .5, False
    files = list(application.asset_folder.glob(f'**/{name}*'))
    # print('-----------files:', files)
    if len(files) == 0:
        print('instrument', name, 'not found')
        return None

    for e in get_tags(files[0].stem, '[', ']'):
        if e.startswith('a'):
            attack = int(e[1:])
            print('set attack to:', e[1:])
        if e.startswith('f'):
            print('set falloff to:', int(e[1:]) / 1000)
            falloff = int(e[1:]) / 1000
        if e == 'loop':
            loop_samples = True

    for f in files:
        for e in get_tags(f.stem, '[', ']'):
            if e.startswith('n'):
                note_num = int(e[1:])
                samples[note_num] = glob.escape(f.stem)

    # print(samples)
    new_samples = [e for e in samples]
    for i, s in enumerate(samples):
        if s != None:
            new_samples[i] = (samples[i], 1)

        else:
            a = 999
            for a in range(0, 128-i):
                if samples[i+a] != None:
                    closest = a
                    break
                a=999

            # distance to sample below
            b = 999
            for b in range(0, i+1):
                if samples[i-b] != None:
                    closest = b
                    break
                b=999

            dist = min(a, b)

            if dist == b:
                dist = -dist

            new_samples[i] = (samples[i+dist], pow(1 / 1.05946309436, dist))
            # new_samples[i] = (samples[i+dist], dist))

    # print(new_samples)
    return new_samples, attack, falloff, loop_samples




if __name__ == '__main__':
    # i = load_instrument('0DefaultPiano')
    # i = load_instrument('celeste')
    from ursina import *
    app = Ursina()
    # Audio('oooooleander')
    import time
    t = time.time()
    files = list(application.asset_folder.glob(f'**/uoiowa_piano*'))
    # print(files)
    print(time.time() - t)
    i = load_instrument('uoiowa_piano')
    for e in i:
        print(e)
    app.run()
