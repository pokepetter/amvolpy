from ursina import application
from pathlib import Path
import note_sheet

from popup_message import PopupMessage


def create(name, path=application.asset_folder/'amvol_projects'):

    path = path / name

    if not path.suffix == '.amvol':
        path = Path(str(path) + '.amvol')

    print('create new project:', path)

    if path.is_file():
        PopupMessage('Error', 'A file already exists with that name \n<yellow>' + str(path), z=-100)
        return False

    notesheet.clear()
    with open(path, 'w+') as f:
        f.write('name = ' + name)

    base.start_screen.close()
    base.top_bar.text = 'Amvol - ' + name



def load(path):
    print('try to load...', path)
    notesheet.clear()

    with open(path, 'r') as f:
        try:
            exec(f.read())

            with open('recent_projects.txt', 'r') as recent:
                recent_files = recent.read().split('\n')

            with open('recent_projects.txt', 'w') as recent:
                for rf in recent_files:
                    if rf.strip() == str(path.resolve()):
                        recent_files.remove(rf)

                if len(recent_files) >= 10:
                    recent_files = recent_files[9:]

                recent_files = [str(path.resolve()), ] + recent_files
                recent_files = [e for e in recent_files if e]
                for rf in recent_files:
                    recent.write(rf + '\n')

        except Exception as e:
            print(e)
        finally:
            base.start_screen.close()
            base.top_bar.text = 'Amvol - ' + path.name
            print('load', path)



if __name__ == '__main__':
    p = Path('.') / 'amvol_projects' / 'test4.amvol'
    load(p)
