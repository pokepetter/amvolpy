from ursina import *



app = Ursina()


from ursina.prefabs.grid_editor import ASCIIEditor
Text.default_font = 'VeraMono.ttf'
# window.color = color.light_gray
# section = ASCIIEditor(size=(16,16), palette=[' ', '*', '-', '_', '.'], color=color.smoke, line_height=.5)
# section.text_entity.color = color.black
# section.scale_y *= .75

# def input(key):
#     if not section.hovered:
#         return
#
#     y = int(round(section.cursor.y * section.h))
#     x = int(round(section.cursor.x * section.w))
#
#     if key == '1':
#         for i in range(32):
#             try:
#                 section.grid[x+i][y] = section.selected_char
#             except:
#                 pass
#         section.record_undo()
#         section.render()

# bar = Draggable(parent=scene, scale=(1,1/16))
camera.orthographic = True
camera.fov = 5
block = Draggable(parent=scene, step=(1,1,0), model='quad', color=color.white, origin=(-.5,.5), scale_y=1/8)
block.content = Entity(parent=block, model='quad', origin=(-.5,.5), y=-1, scale_y=8, color=color.gray)
block.small_grid = Entity(parent=block.content, model=Grid(16,16), origin=(-.5,.5), color=color.color(0,0,1,.1), z=-.1)
block.quarter_note_grid = Entity(parent=block.content, model=Grid(4,1), origin=(-.5,.5), color=color.white66, z=-.1)
block.whole_note_grid = Entity(parent=block.content, model=Grid(1,1), origin=(-.5,.5), color=color.cyan, z=-.1)

def add_loops(block, value):
    print(block)
    block.scale_x += value
    block.small_grid.model = Grid(block.scale_x * 16, 16)
    block.small_grid.origin = (-.5,.5)
    block.quarter_note_grid.model = Grid(block.scale_x * 4, 16)
    block.quarter_note_grid.origin = (-.5,.5)
    block.whole_note_grid.origin = (-.5,.5)
    block.plus.world_scale = 1/8
    print('----', ((0,0), (0,1),) * int(block.scale_x))
    block.whole_note_grid.model = Mesh(vertices=((0,0), (0,1),) * int(block.scale_x), thickness=4)


block.plus = Button(parent=block, text='+', model='circle', world_scale=1/8, z=-.1, origin=(.5,.5), x=1, color=color.red)
block.plus.text_entity.world_scale = .25
block.plus.text_entity.position = (-.5,-.5)
block.plus.on_click = Func(add_loops, block, 1)
# t = Text(parent=e, text='> M intro', z=-.2, scale=2.5, color=color.black)

app.run()
