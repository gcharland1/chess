import chessman

class ChessSet:
    chessman_number = {
        'pawn': 8,
        'rook': 2,
        'knight': 2,
        'bishop': 2,
        'queen': 1,
        'king': 1,
    }

    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']

    def __init__(self):
        self.board = [['' for i in range(8)] for j in range(8)]
        self.populate_board()

    def populate_board(self):
        for c in range(8):
            self.board[1][c] = chessman.Chessman('b', 'pawn')
            self.board[6][c] = chessman.Chessman('w', 'pawn')

        for r in [0, 7]:
            if r == 7:
                color = 'w'
            else:
                color = 'b'

            self.board[r][0] = chessman.Chessman(color, 'rook')
            self.board[r][1] = chessman.Chessman(color, 'knight')
            self.board[r][2] = chessman.Chessman(color, 'bishop')
            self.board[r][3] = chessman.Chessman(color, 'king')
            self.board[r][4] = chessman.Chessman(color, 'queen')
            self.board[r][5] = chessman.Chessman(color, 'bishop')
            self.board[r][6] = chessman.Chessman(color, 'knight')
            self.board[r][7] = chessman.Chessman(color, 'rook')

    def move(self, r1, c1, r2, c2):
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = ''

    def is_chessman(self, row, col):
        if type(self.board[row][col]) == chessman.Chessman:
            return True
        else:
            return False

def cmd_display(set):
    print('\n\n\t' + '|----'*8 + '|')
    for r in range(8):
        print('\t|', end='')
        for c in range(8):
            p = set.board[r][c]
            if type(p) == chessman.Chessman:
                print(f'{p.color}{p.type[0]}'.center(4), end='|')
            else:
                print(p.center(4), end='|')
        print(set.rows[r].center(3), end='')
        print('\n\t' + '|----'*8 + '|')
    print('\t ', end='')
    for c in range(8):
        print(set.cols[c].center(5), end='')
    print('\n')

if __name__ == '__main__':
    set = ChessSet()
    cmd_display(set)
    set.move(6, 4, 4, 4)
    set.move(1, 2, 3, 2)
    cmd_display(set)
