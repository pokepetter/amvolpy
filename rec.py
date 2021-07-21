from ursina import *
from note_section import NoteSection
import scalechanger
import main


parent = None
types = list()

current_note_section = None
recording = False
# indicator = Entity(model='quad', scale_x=.01, color=color.azure)


def start_recording():
    # get tempo before recotding
    # find open space
    global current_note_section
    global recording
    # global indicator
    current_note_section = NoteSection(x=0, y=0/64)
    current_note_section.end_button.x = 100
    current_note_section.end_button.drop()
    # current_note_section.indicator.animate
    current_note_section.play()
    recording = True
    main.stop_record_button.enabled = True


def stop_recording():
    global current_note_section
    global recording
    # global indicator
    main.stop_record_button.enabled = False
    recording = False
    current_note_section.end_button.x = current_note_section.indicator.x
    current_note_section.end_button.drop()
    current_note_section.loop_button.x = max(current_note_section.indicator.x, .1)
    current_note_section.loop_button.drop()
    current_note_section.stop()

    if not current_note_section.notes:
        destroy(current_note_section)

    current_note_section = None




def input(key):
    global current_note_section

    if held_keys['control'] and key == 'r':
        if not recording:
            start_recording()
        else:
            stop_recording()

    # recording, start note
    elif recording:
        for i, k in enumerate(base.keyboard.keys):
            if key == k:
                note_num = i + (base.keyboard.octave_offset * len(scalechanger.pattern))
                note_num = scalechanger.note_offset(note_num)

                x = current_note_section.indicator.x * current_note_section.scale_x
                note = current_note_section.add_note(x=x, y=i, strength=1, length=0)

            if key == k + ' up':
                # print('stop:', i)
                octave = i//16
                fresh_notes = [n for n in current_note_section.notes if n.length == 0]
                if fresh_notes:
                    fresh_notes[0].length = (current_note_section.indicator.x * current_note_section.scale_x) - fresh_notes[0].x

                current_note_section.draw_notes()

scene.entities.append(sys.modules['rec'])
