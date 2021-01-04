class Chessman:
    def __init__(self, color, type, starting_position):
        self.color = color
        self.type = type
        self.position = starting_position
        self.notation_letter = self.notation_letter()
        self.active = False
        self.valid_moves = []
        self.image = self.color + "_" + self.type + '.png'


    def notation_letter(self):
        if self.type == 'knight':
            return self.type[1].capitalize()
        else:
            return self.type[0].capitalize()

