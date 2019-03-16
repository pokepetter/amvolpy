from ursina import *

class SaveSystem(Entity):
    def input(self, key):
        if held_keys['control'] and key == 's':
            self.save()

        if held_keys['control'] and key == 'o':
            self.load()

    def save(self, path=None):
        print('SAVING!')
        if not path:
            # print(ask for name)
            path = application.asset_folder / 'test_save.py'

        f = ''
        for ns in [e for e in scene.entities if e.type == 'NoteSection']:
            f += str(ns) + '\n'

        with open(path, 'w') as file:
            print(f)
            file.write(f)



    def load(self, path=None):
        print('load')
        if not path:
            # print(ask for name)
            path = application.asset_folder / 'test.py'

        base.notesheet.new_project()
        with open(path, 'r') as file:
            exec(file.read())
            file.read()


self = SaveSystem()
sys.modules[__name__] = self


if __name__ == '__main__':
    app = Ursina()

    app.run()
