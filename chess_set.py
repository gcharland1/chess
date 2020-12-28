import chess_board
import chessman

class chess_set:
    chessman_number = {
        'pawn': 8,
        'rook': 2,
        'knight': 2,
        'bishop': 2,
        'queen': 1,
        'king': 1,
    }

    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        print(self.board)
        self.create_chessmen()
        self.populate_board()

    def create_chessmen(self):
        self.blacks = []
        self.whites = []
        for type, qty in self.chessman_number.items():
            for n in range(0, qty):
                self.whites.append(chessman.chessman('white', type))
                self.blacks.append(chessman.chessman('black', type))

    def populate_board(self):
        for c in range(8):
            self.board[6][c] = chessman.chessman('black', 'pawn')
            self.board[1][c] = chessman.chessman('white', 'pawn')

        for r in [0, 7]:
            if r == 0:
                color = 'white'
            else:
                color = 'black'
            self.board[r][0] = chessman.chessman(color, 'rook')
            self.board[r][1] = chessman.chessman(color, 'knight')
            self.board[r][2] = chessman.chessman(color, 'bishop')
            self.board[r][3] = chessman.chessman(color, 'queen')
            self.board[r][4] = chessman.chessman(color, 'king')
            self.board[r][5] = chessman.chessman(color, 'bishop')
            self.board[r][6] = chessman.chessman(color, 'knight')
            self.board[r][7] = chessman.chessman(color, 'rook')

set = chess_set()
for r in set.board:
    for p in r:
        try:
            print(f'{p.color[0]}{p.type[0]}'.center(5), end='')
        except:
            print('X'.center(5), end='')
    print('\n')
