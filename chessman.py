class Chessman:
    def __init__(self, color, type):
        self.type = type
        self.notation_letter = self.notation_letter()
        self.color = color
        self.active = False
        self.valid_moves = []
        self.possible_moves = self.all_possible_moves()
        self.image = self.color + "_" + self.type + '.png'

    def all_possible_moves(self):
        moves = []
        if self.type == 'knight':
            moves = [[1, 2], [1, -2], [-1, -2], [-1, 2], [2, 1], [2, -1], [-2, 1], [-2, -1]]

        elif self.type == 'king':
            moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1], [0, -2], [0, 2]]

        elif self.type == 'bishop':
            for l in range(8):
                moves.append([l, l])
                moves.append([l, -l])
                moves.append([-l, l])
                moves.append([-l, -l])

        elif self.type == 'queen':
            for l in range(8):
                moves.append([l, 0])
                moves.append([-l, 0])
                moves.append([0, l])
                moves.append([0, -l])
                moves.append([l, l])
                moves.append([l, -l])
                moves.append([-l, l])
                moves.append([-l, -l])

        elif self.type == 'rook':
            for l in range(8):
                moves.append([l, 0])
                moves.append([-l, 0])
                moves.append([0, l])
                moves.append([0, -l])

        return moves

    def notation_letter(self):
        if self.type == 'knight':
            return self.type[1].capitalize()
        else:
            return self.type[0].capitalize()

if __name__ == '__main__':
    print(Chessman('w', 'pawn').allowed_moves())
