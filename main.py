import pygame
import chess_set

def main():
    set = chess_set.ChessSet()

    root = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption('Chess Game')
    bg = pygame.image.load(IMAGE_DIR + BG_IMAGE)

    whos_turn = 'w'
    r1, c1 = (-1, -1)

    running = True
    update_display(root, bg, set, whos_turn)

    while running:
        update = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                r1, c1, whos_turn = make_move(set, event.pos, whos_turn, r1, c1)
                print(f"Possible moves are: {set.board[r1][c1].valid_moves}")
                update = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    whos_turn = undo_move(set, whos_turn)
                    update = True
                if event.key == pygame.K_r:
                    whos_turn = new_game(set)
                    update = True
                if event.key == pygame.K_m:
                    print('Display Menu')

            if event.type == pygame.QUIT:
                running = False

        if update:
            update_display(root, bg, set, whos_turn)
            set.set_valid_moves()

    pygame.display.quit()
    return False

def update_display(root, bg, set, whos_turn):
    if whos_turn == 'w':
        color = 'White'
    else:
        color = 'Black'
    caption = f'Chess Game - {color} to play'
    pygame.display.set_caption(caption)
    root.blit(bg, (0, 0))
    for r in range(len(set.board)):
        for c in range(len(set.board)):
            if set.is_chessman(r, c):
                img = set.board[r][c].image
                x = int(SQ_W*c + 2)
                y = int(SQ_H*r + 2)
                root.blit(pygame.image.load(IMAGE_DIR + img), (x, y))

    pygame.display.update()

def get_board_index(pos):
    c = int(pos[0]/SQ_W)
    r = int(pos[1]/SQ_H)
    return (r, c)

def make_move(set, event_pos, whos_turn, r1, c1):
    if (r1, c1) == (-1, -1):
        r, c = get_board_index(event_pos)
        if set.is_players_piece(r, c, whos_turn):
            return r, c, whos_turn
        else:
            print('Please pick a valid piece. Look at caption to see which color plays.')
            return -1, -1, whos_turn
    else:
        r2, c2 = get_board_index(event_pos)
        if [r2, c2] in set.board[r1][c1].valid_moves:
            set.move(r1, c1, r2, c2)
            whos_turn = switch_teams(whos_turn)
        else:
            print('Invalid Move')

        r1, c1 = -1, -1

    return r1, c1, whos_turn

def undo_move(set, whos_turn):
    undid = set.undo()
    if undid:
        switch_teams(whos_turn)
    else:
        return whos_turn

def switch_teams(team):
    if team == 'w':
        return 'b'
    else:
        return 'w'

def new_game(set):
    set.reset_board()
    return 'w'


IMAGE_DIR = './images/'
BG_IMAGE = 'chessboard.png'
APP_WIDTH, APP_HEIGHT = (800, 800)
SQ_W = int(APP_WIDTH/8)
SQ_H = int(APP_HEIGHT/8)

PLAYER = 'b' # Players plays black. Need to change display mechanics to allow player to face blacks

if __name__=='__main__':
    main()
