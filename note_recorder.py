from ursina import *
if __name__ == '__main__':
    app = Ursina()


from note_section import NoteSection
import scale_changer
import note_sheet


current_note_section = None
recording = False
waiting_for_input = False


def start_recording(count_down=False, wait_for_input=True):
    global current_note_section
    record_button.enabled = False
    stop_recording_button.enabled = True
    # return
    # get tempo before recotding
    # find open space
    current_note_section = NoteSection(x=0, y=0/64)
    current_note_section.end_button.x = 100
    current_note_section.end_button.drop()
    current_note_section.selected = True
    # current_note_section.indicator.animate
    # if count_down:
    #     invoke(print_on_screen, '<red>1', position=(0,0), origin=(0,0), duration=.02, delay=0)
    #     invoke(print_on_screen, '<red>2', position=(0,0), origin=(0,0), duration=.02, delay=0.5)
    #     invoke(print_on_screen, '<red>3', position=(0,0), origin=(0,0), duration=.02, delay=1.0)
    #     invoke(print_on_screen, '<red>4', position=(0,0), origin=(0,0), duration=.02, delay=1.5)
    #     invoke(current_note_section.play, delay=2)
    #     invoke(setattr, 'recording', True, delay=2)
    #     return
    #
    # elif wait_for_input:
    #     waiting_for_input = True
    #     recording = True
    #
    # else:
    current_note_section.play()
    recording = True
    note_sheet.play()
    print('started recording')


def stop_recording():
    global current_note_section
    stop_recording_button.enabled = False
    record_button.enabled = True

    recording = False
    waiting_for_input = False
    # print('---------------------', current_note_section.indicator.x)
    current_note_section.end_button.x = current_note_section.indicator.x
    current_note_section.end_button.drop()
    current_note_section.loop_button.x = max(current_note_section.indicator.x, .1)
    current_note_section.loop_button.drop()
    current_note_section.stop()

    if not current_note_section.notes:
        destroy(current_note_section)

    current_note_section = None
    note_sheet.stop()


def input(key):

    if held_keys['control'] and key == 'r':
        if not recording:
            start_recording()
        else:
            stop_recording()


def start_note(y, velocity=1):
    if waiting_for_input:
        note_sheet.play()
        waiting_for_input = False

    # play note
    note_num = scale_changer.note_offset(y)
    current_note_section.play_note(note_num, velocity)

    #record note
    # print('start recording note:', y)
    x = current_note_section.indicator.x * current_note_section.scale_x
    note = current_note_section.add_note(x=x, y=y, strength=velocity, length=0)


def stop_note(y):
    fresh_notes = [n for n in current_note_section.notes if n.length == 0]
    if fresh_notes:
        fresh_notes[0].length = (current_note_section.indicator.x * current_note_section.scale_x) - fresh_notes[0].x

    current_note_section.stop_note(y)
    current_note_section.draw_notes()


record_button = Button(parent=camera.ui, scale=.055, z=-2, y=-.45+.0125, text='<image:arrow_right>', color=color.red,
    tooltip=Tooltip('Record'), on_click=Func(start_recording, count_down=False))

stop_recording_button = Button(parent=camera.ui, scale=.055, y=-.45+.0125, z=-1.1, color=color.azure, text='||',
    tooltip=Tooltip('Stop recording'), on_click=stop_recording, enabled=False)



if __name__ == '__main__':
    # import main
    import keyboard

    import scale_changer_menu
    # from note_sheet import NoteSheet
    # note_sheet = NoteSheet()
    camera.orthographic = True
    camera.fov = 6
    camera.x = camera.fov * .875
    camera.y = camera.fov * .375
    app.run()
