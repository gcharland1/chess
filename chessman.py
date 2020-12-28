class Chessman:
    def __init__(self, color, type):
        self.type = type
        self.color = color
        self.active = False
        self.image = color + "_" + type + '.png'

if __name__ == '__main__':
    Chessman('b', 'king')
