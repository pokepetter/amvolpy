class Note:

    default_length = .125

    def __init__(self, x, y, length=default_length, strength=1):
        self.x = x
        self.y = y
        self.length = length
        self.strength = strength


    def __str__(self):
        # return f'Note(x={self.x}, y={self.y}, length={self.length}, strength={self.strength})'
        return f'Note({self.x}, {self.y}, {self.length}, {self.strength})'



if __name__ == '__main__':
    print(Note(0,0))
