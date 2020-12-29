import chessman
import copy


class ChessSet:

    cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows = ['8', '7', '6', '5', '4', '3', '2', '1']

    def __init__(self):
        self.reset_board()
        self.current_move = 0.0
        self.move_log = []

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
            self.board[r][3] = chessman.Chessman(color, 'queen')
            self.board[r][4] = chessman.Chessman(color, 'king')
            self.board[r][5] = chessman.Chessman(color, 'bishop')
            self.board[r][6] = chessman.Chessman(color, 'knight')
            self.board[r][7] = chessman.Chessman(color, 'rook')

    def reset_board(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.move_log = []
        self.current_move = 0.0

    def move(self, r1, c1, r2, c2):
        self.update_log()
        self.current_move += 0.5

        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = ''
        self.board[r2][c2].active = True


    def undo(self):
        if self.current_move > 0:
            self.board = self.move_log.pop(-1)
            self.current_move -= 0.5
            return True
        else:
            print('Initial state, cannot undo further')
            return False

    def update_log(self):
        current_state = []
        for i in range(len(self.board)):
            row = []
            for j in range(len(self.board[0])):
                row.append(copy.deepcopy(self.board[i][j]))
            current_state.append(row)

        self.move_log.append(current_state)

    def is_chessman(self, row, col):
        if type(self.board[row][col]) == chessman.Chessman:
            return True
        else:
            return False

    def is_valid_piece(self, row, col, player_color):
        valid_piece = False
        if self.is_chessman(row, col):
            if self.board[row][col].color == player_color:
                valid_piece = True

        return valid_piece

    def is_valid_move(self, r1, c1, r2, c2, player_color):
        played_piece = self.board[r1][c1]
        move = [r2-r1, c2-c1]
        valid_move = True
        take = False
        if self.is_chessman(r2, c2):
            if self.board[r2][c2].color == player_color:
                return False
            else:
                take = True

        if not move in played_piece.allowed_moves(take):
            return False

        if not played_piece.type == 'knight':
            move_length = max(abs(move[0]), abs(move[1]))
            axis = [int(move[0]/move_length), int(move[1]/move_length)]
            for i in range(1, move_length):
                ri = r1 + axis[0]*i
                ci = c1 + axis[1]*i
                if self.is_chessman(ri, ci):
                    print(f"There's interference at {self.cols[ci]}{self.rows[ri]}")
                    return False

        return valid_move

def cmd_display(board_state):
    print('\n\n\t' + '|----'*8 + '|')
    for r in range(8):
        print('\t|', end='')
        for c in range(8):
            p = board_state[r][c]
            if type(p) == chessman.Chessman:
                if p.type == 'knight':
                    print(f'{p.color}{p.type[1]}'.center(4), end='|')
                else:
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
    set.move(6, 3, 4, 3)
    cmd_display(set.board)
    set.move(1, 3, 3, 3)
    cmd_display(set.board)
    set.undo()
    cmd_display(set.board)
    set.undo()
    cmd_display(set.board)
