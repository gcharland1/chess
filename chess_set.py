import chessman
import chess_player
import copy


class ChessSet:

    cols_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    rows_numbers = ['8', '7', '6', '5', '4', '3', '2', '1']

    def __init__(self):
        self.white_player = chess_player.ChessPlayer('w')
        self.black_player = chess_player.ChessPlayer('b')
        self.who_plays = self.white_player
        self.reset_board()
        self.current_move = 0.0
        self.move_log = []

    def populate_board(self):
        for c in range(8):
            self.board[1][c] = chessman.Chessman('b', 'pawn', [1, c])
            self.board[6][c] = chessman.Chessman('w', 'pawn', [6, c])

        for r in [0, 7]:
            if r == 7:
                color = 'w'
            else:
                color = 'b'

            self.board[r][0] = chessman.Chessman(color, 'rook', [r, 0])
            self.board[r][1] = chessman.Chessman(color, 'knight', [r, 1])
            self.board[r][2] = chessman.Chessman(color, 'bishop', [r, 2])
            self.board[r][3] = chessman.Chessman(color, 'queen', [r, 3])
            self.board[r][4] = chessman.Chessman(color, 'king', [r, 4])
            self.board[r][5] = chessman.Chessman(color, 'bishop', [r, 5])
            self.board[r][6] = chessman.Chessman(color, 'knight', [r, 6])
            self.board[r][7] = chessman.Chessman(color, 'rook', [r, 7])

    def define_teams(self):
        whites = []
        blacks = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.is_chessman(i, j):
                    if self.board[i][j].color == 'w':
                        whites.append(self.board[i][j])
                    else:
                        blacks.append(self.board[i][j])

        self.white_player.pieces = whites
        self.black_player.pieces = blacks

    def reset_board(self):
        self.board = [['' for _ in range(8)] for _ in range(8)]
        self.populate_board()
        self.define_teams()
        self.set_valid_moves()

        self.current_move = 0.0
        self.move_log = []

    def make_move(self, r1, c1, r2, c2):
        if not self.is_chessman(r1, c1):
            return
        self.update_log()
        self.current_move += 0.5
        played_piece = self.board[r1][c1]
        if self.is_chessman(r2, c2):
            taken_piece = self.board[r2][c2]
            if self.who_plays == self.white_player:
                self.black_player.pieces.remove(taken_piece)
            else:
                self.white_player.pieces.remove(taken_piece)

        played_piece.active = True
        played_piece.position = [r2, c2]
        self.toggle_player()

    def move(self, r1, c1, r2, c2):
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = ''

    def toggle_player(self):
        if self.who_plays == self.white_player:
            self.who_plays = self.black_player
        else:
            self.who_plays = self.white_player

    def undo(self):
        if self.current_move > 0:
            self.board = self.move_log.pop(-1)
            self.define_teams()
            self.set_valid_moves()
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
        for player in [self.white_player, self.black_player]:
            for piece in player.pieces:
                self.list_valid_moves(piece)

    def list_valid_moves(self, piece):
        row, col = piece.position
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
            for move in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
                r2 = row + move[0]
                c2 = col + move[1]
                moves_inbound = r2 in range(8) and c2 in range(8)
                if moves_inbound and not self.is_players_piece(r2, c2, piece.color) and not self.is_check(r2, c2, piece.color):
                    move_list.append([r2, c2])
            # Add castle mechanics

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
                    moves_inbound = r2 in range(8) and c2 in range(8)
                    if moves_inbound and not self.is_players_piece(r2, c2, piece.color):
                        move_list.append([r2, c2])
                        if self.is_chessman(r2, c2):
                            break
                    else:
                        break


        piece.valid_moves = move_list
        return move_list

    def is_check(self, row, col, color):
        if color == 'w':
            opponents = self.black_player.pieces
        else:
            opponents = self.white_player.pieces

        for opp in opponents:
            if [row, col] in opp.valid_moves:
                return True

        return False


#############################
### End of class ChessSet ###
#############################

def cmd_display(chess):

    board_state = chess.board

    print('\n\n\t' + '|----'*8 + '|')
    for r in range(8):
        print('\t|', end='')
        for c in range(8):
            p = board_state[r][c]
            if chess.is_chessman(r, c):
                print(f'{p.color}{p.notation_letter}'.center(4), end='|')
            else:
                print(p.center(4), end='|')
        print(chess.rows_numbers[r].center(3), end='')
        print('\n\t' + '|----'*8 + '|')
    print('\t ', end='')

    for c in range(8):
        print(chess.cols_letters[c].center(5), end='')
    print('\n')

if __name__ == '__main__':
    set = ChessSet()
    set.move(0, 3, 5, 1)
    cmd_display(set)
    set.set_valid_moves()
    print(set.board[5][1].valid_moves)