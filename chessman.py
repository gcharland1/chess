class Chessman:
    def __init__(self, color, type):
        self.type = type
        self.color = color
        self.active = False
        self.image = color + "_" + type + '.png'

    def allowed_moves(self, is_a_take):
        moves = []
        if self.type == 'pawn':
            if self.color == 'b':
                if is_a_take:
                    moves.append([1, 1])
                    moves.append([1, -1])
                else:
                    moves.append([1, 0])
                    if not self.active:
                        moves.append([2, 0])
            else:
                if is_a_take:
                    moves.append([-1, 1])
                    moves.append([-1, -1])
                else:
                    moves.append([-1, 0])
                    if not self.active:
                        moves.append([-2, 0])

        elif self.type == 'knight':
            moves = [[1, 2], [1, -2], [-1, -2], [-1, 2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        elif self.type == 'king':
            moves = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

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

        return moves


if __name__ == '__main__':
    print(Chessman('w', 'pawn').allowed_moves())
