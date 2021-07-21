from ursina import *

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 1


composer = Entity(position=(-.85, -.5+.05,1),
    # model=Circle(radius=.005),
    )
composer.bg = Entity(model='quad', color=color._64, origin_y=.5, z=2, scale=10)
composer.grid = Entity(parent=composer, scale=(.4*4,.4), model=Grid(8*4,8), origin=(-.5,-.5), color=color._84)

class NoteSection(Draggable):
    def __init__(self, **kwargs):
        super().__init__(parent=composer, model='quad', origin=(-.5,-.5), step=(.1/4,.1,0), color=color.azure, scale=.05)
        self.step = (self.scale_x/4, self.scale_y, 0    )
        self.outline = Entity(parent=self, model=Quad(mode='line', radius=0), origin=self.origin)
        self.drag_bar = Draggable(parent=composer, model='quad', origin=(.5,-.5), z=-.1, step=self.step, color=color.yellow, scale=(.005,self.scale_y))
        self.note_dict = {}

    def update(self):
        super().update()
        if self.drag_bar.dragging:
            self.scale_x = self.drag_bar.world_x - self.world_x
            self.drag_bar.world_scale_x = .05
        else:
            self.drag_bar.x = self.x + self.scale_x
            self.drag_bar.y = self.y


current_note_section = NoteSection()


note_editor = Entity(model='quad', color=color.black, origin=(-.5,-.5), x=-.475*window.aspect_ratio, scale_x=.475*window.aspect_ratio*2, scale_y=.8, collider='box', z=2)
h = 7*7
w = int(.475*window.aspect_ratio*2*64)

# scale_y = scale_x
grid = Entity(parent=note_editor, model=Grid(w,h), origin=(-.5,-.5), position=(0,0), z=-1, color=color._32)
note_names = '\n'.join(('1234567'*7))
t = Text(parent=note_editor, origin=(.5,.5), font='VeraMono.ttf', text=note_names, z=-1, position=(-.505,1), world_scale=10)

note_editor.add_script(Scrollable())
note_renderer = Entity(parent=note_editor, z=-.1, model=Mesh(vertices=[], mode='point', thickness=.01), texture='circle', x=1/w/2, y=1/h/2)
note_editor.cursor = Entity(model='quad', parent=note_editor, scale=(1/128, 1/h), origin=(-.5,-.5), color=color.azure, z=-1)


def update():
    if note_editor.hovered:
        # cursor.position = mouse.point
        x = int(mouse.point.x * w) / w
        y = int(mouse.point.y * h) / h
        note_editor.cursor.position = Vec3(x,y,-1)
        # print(cursor.y)
        name = f'{x},{y}'

        if mouse.left:
            if not name in current_note_section.note_dict:
                current_note_section.note_dict[name] = Vec3(x,y,0)

        elif mouse.right:
            if name in current_note_section.note_dict:
                del current_note_section.note_dict[name]


        note_renderer.model.vertices = []
        for key, value in current_note_section.note_dict.items():
            note_renderer.model.vertices.append(value)

            # print(grid_pos)
        note_renderer.model.generate()

    # def render(self):
    #     self.note_renderer.generate()


    # def on_click(self):



class MiddleBar(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, model='quad', origin_y=.5, collider='box', color=color._16, scale=(camera.aspect_ratio,.05), z=-2, y=.0)




    # NoteEditor()
MiddleBar()
if __name__ == '__main__':
    app.run()
