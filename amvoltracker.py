from ursina import *
from time import perf_counter

app = Ursina()



camera.orthographic = True
camera.fov = 32

e = Entity(model='quad', collider='box', color=color.black, scale=32)
grid = Entity(parent=e, model=Grid(32,32), color=color._32, z=-.1)
cursor = Entity(model='wireframe_quad', origin=(-.5,-.5))

offset = 30
keys = 'zxcvbnm,.asdfghjklqwertyuio1234567890'

t = perf_counter()

num_tracks = 32

notes = [[None for y in range(num_tracks)] for x in range(32)]

renderers = [[None for y in range(num_tracks)] for x in range(32)]

a = Audio('sine', loop=True, volume=0)
from copy import copy, deepcopy
# instruments = [Audio(a.clip, loop=True, volume=0) for i in range(num_tracks)]
instruments = [Audio('sine', loop=True, volume=0) for i in range(num_tracks)]

print('----', perf_counter() - t)

app.playing = False
app.t = 0
app.i = 0

def input(key):
    if key in keys or key == ' ':
        if key == ' ':
            n = 0
        else:
            n = keys.index(key)

        if e.hovered:
            coord = mouse.point
            x = int((coord[0] + .5) * 32)
            y = int((coord[1] + .5) * 32)

            print('aaaaaaaa', x,y)
            cursor.position = (-16+x,-16+y, -.1)

            if n:
                n = offset + n

                import scale_changer
                scale_changer.pattern = (3,2,2,3,2)
                n = scale_changer.note_offset(n) - 20


            instruments[y].fade(1, duration=0)
            instruments[y].fade(0, delay=1/8)
            diff = (possible_note_frequencies[n] - 440)
            pitch = 1 + (diff / 440)
            instruments[y].pitch = pitch


            if mouse.left:
                notes[x][y] = n

                if not renderers[x][y]:
                    renderers[x][y] = Text(parent=e, position=(-.5+(x/32),-.5+(y/num_tracks), -.1), text='<dark_gray>0', origin=(-.5,-.5), scale=.5)
                renderers[x][y].text = f'<white>{i}'
                if n == 0:
                    renderers[x][y].text = f'<white>|'



    if key == 'space':
        app.playing = not app.playing
        if not app.playing:
            app.t = 0
            app.i = 0
            for _ in instruments:
                _.volume = 0


line = Entity(model='quad', scale=(1,num_tracks), origin=(-.5,-.5), color=color.azure, alpha=.3, x=-16, y=-16, z=-.1)
def update():
    if app.playing:
        app.t += time.dt
        if app.t >= 1/8:
            app.t = 0
            app.i += 1
            if app.i >= num_tracks:
                app.i = 0

            # print(app.i)
            for i, n in enumerate(notes[app.i]):
                if n == None:
                    continue

                if n > 0:
                    instruments[i].volume = 1

                    # import scale_changer
                    # scale_changer.pattern = (3,2,2,3,2)
                    # n = scale_changer.note_offset(n) - 20
                    print('----', n)

                    diff = (possible_note_frequencies[n] - 440)
                    pitch = 1 + (diff / 440)
                    instruments[i].pitch = pitch

                else:
                    instruments[i].volume = 0

            line.x = -16 + app.i


start_hz = 440
note_index = 69 # A4
twelfth_root_of_two = pow(2, 1/12)

possible_note_frequencies = [440 for i in range(128)]
for i in range(128):
    possible_note_frequencies[i] = start_hz * pow(twelfth_root_of_two, i-69)
print(possible_note_frequencies)


# def press_note(i, volume=1, length=1/4):
#     import scale_changer
#     scale_changer.pattern = (3,2,2,3,2)
#     i = scale_changer.note_offset(i) - 20
#
#     diff = (possible_note_frequencies[i+offset] - 440)
#     pitch = 1 + (diff / 440)
#     play_note(pitch, length=length, volume=volume)


# def play_note(pitch, length=1/8, volume=1):
#     print(volume)
    # a = Audio('0_default_piano_n48', loop=True, pitch=pitch, volume=volume)
    # a.fade_out(duration=length)


app.run()
