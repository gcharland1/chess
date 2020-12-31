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

    def define_teams(self):
        self.whites = []
        self.blacks = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.is_chessman(i, j):
                    if self.board[i][j].color == 'w':
                        self.whites.append(self.board[i][j])
                    else:
                        self.blacks.append(self.board[i][j])

    def reset_board(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.define_teams()
        self.set_valid_moves()
        self.move_log = []
        self.current_move = 0.0

    def move(self, r1, c1, r2, c2):
        self.update_log()
        self.current_move += 0.5
        played_piece = self.board[r1][c1]
        if self.is_chessman(r2, c2):
            taken_piece = self.board[r2][c2]
            if taken_piece in self.whites:
                self.whites.remove(taken_piece)
            else:
                self.blacks.remove(taken_piece)

        self.board[r2][c2] = played_piece
        self.board[r1][c1] = ''
        played_piece.active = True

    def undo(self):
        if self.current_move > 0:
            self.board = self.move_log.pop(-1)
            self.define_teams()
            self.current_move -= 0.5
            return True
        else:
            print('Initial state, cannot undo further')
            return False

    def update_log(self):
        self.move_log.append(copy.deepcopy(self.board))

    def is_chessman(self, row, col):
        if type(self.board[row][col]) == chessman.Chessman:
            return True
        else:
            return False

    def is_players_piece(self, row, col, player_color):
        players_piece = False
        if self.is_chessman(row, col):
            if self.board[row][col].color == player_color:
                players_piece = True

        return players_piece

    def set_valid_moves(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.is_chessman(r, c):
                    self.list_possible_moves(r, c)


    def list_possible_moves(self, row, col):
        piece = self.board[row][col]
        move_list = []

        if piece.type == 'pawn':
            if piece.color == 'b':
                axis = 1
            else:
                axis = -1

            if not self.is_chessman(row + axis, col):
                move_list.append([row + axis, col])

            if not piece.active and not self.is_chessman(row + 2 * axis, col) and not self.is_chessman(row + axis, col):
                move_list.append([row + 2 * axis, col])

            can_take_right = False
            can_take_left = False
            if col + 1 < 8:
                can_take_right = self.is_chessman(row + axis, col + 1) and not self.is_players_piece(row + axis, col + 1, piece.color)
            if col - 1 >= 0:
                can_take_left = self.is_chessman(row + axis, col - 1) and not self.is_players_piece(row + axis, col - 1, piece.color)

            if can_take_right:
                move_list.append([row + axis, col + 1])
            if can_take_left:
                move_list.append([row + axis, col - 1])

        elif piece.type == 'knight':
            possible_directions = [[1, 2], [1, -2], [-1, -2], [-1, 2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
            for move in possible_directions:
                r2 = row + move[0]
                c2 = col + move[1]
                if r2 in range(8) and c2 in range(8) and not self.is_players_piece(r2, c2, piece.color):
                    move_list.append([r2, c2])

        elif piece.type == 'king':
            move_list = []

        else:
            if piece.type == 'queen':
                axes = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
            elif piece.type == 'bishop':
                axes = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
            elif piece.type == 'rook':
                axes = [[0, 1], [0, -1], [1, 0], [-1, 0]]

            for axis in axes:
                for l in range(1, 8):
                    r2 = row + l*axis[0]
                    c2 = col + l*axis[1]
                    if r2 in range(8) and c2 in range(8) and not self.is_players_piece(r2, c2, piece.color):
                        move_list.append([r2, c2])
                        if self.is_chessman(r2, c2):
                            break
                    else:
                        break


        piece.valid_moves = move_list
        return move_list


#############################
### End of class ChessSet ###
#############################

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
    set.move(1, 1, 5, 1)
    cmd_display(set.board)
    set.set_valid_moves()
    print(f"White moves are: {set.board[6][1].valid_moves}")
    print(f"Black moves are: {set.board[5][1].valid_moves}")