from pandaeditor import *


class Save(Entity):
    def input(self, key):
        if held_keys['control'] and key == 's':
            self.save()

        if held_keys['control'] and key == 'o':
            self.load()

    def save(self, path=None):
        if not path:
            # print(ask for name)
            path = application.asset_folder + 'test' + '.py'

        f = '''
from pandaeditor import *
from notesection import NoteSection
from note import Note
'''
        for ns in base.notesheet.note_sections:
            f += f'''
{ns.type}(
    position=({ns.x}, {ns.y}),
    # color={ns.color},
    sound='{ns.sound.getName().split('.')[0]}',
    end={ns.end_button.x},
    loop_end={ns.loop_button_end.x},
    notes=(
'''
            for note in [n for n in ns.note_parent.children if n.type == 'Note']:
                f += f'''        Note(x={note.x}, y={note.y}, length={note.length}, strength={note.strength}),\n'''

            f += '''
    )
)'''

        with open(path, 'w') as file:
            print(f)
            file.write(f)



    def load(self, path=None):
        print('load')
        if not path:
            # print(ask for name)
            path = application.asset_folder + 'test' + '.py'

        base.notesheet.new_project()
        with open(path, 'r') as file:
            exec(file.read())
            file.read()


sys.modules[__name__] = Save()
