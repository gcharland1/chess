import pygame
import chess_set

def main():
    set = chess_set.ChessSet()

    root = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption('Chess Game')
    bg = pygame.image.load(IMAGE_DIR + BG_IMAGE)

    whos_turn = 'w'
    r1, c1 = [-1, -1]

    running = True
    update_display(root, bg, set, r1, c1)

    while running:
        update = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                r1, c1 = make_move(set, event.pos, r1, c1)
                update = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    undid = set.undo()
                    r1 = -1
                    c1 = -1
                    update = True

                if event.key == pygame.K_r:
                    set.reset_board()
                    update = True

                if event.key == pygame.K_m:
                    print('Display Menu')

            if event.type == pygame.QUIT:
                running = False

        if update:
            update_display(root, bg, set, r1, c1)
            set.set_players_moves()

    pygame.display.quit()
    return False

def update_display(root, bg, set, r1, c1):
    if set.who_plays.color == 'w':
        color = 'White'
    else:
        color = 'Black'
    caption = f'Chess Game - {color} to play'
    pygame.display.set_caption(caption)

    root.blit(bg, (0, 0))
    for team in [set.white_player, set.black_player]:
        for piece in team.pieces:
            img = piece.image
            r, c = piece.position
            x = int(SQ_W * c + 2)
            y = int(SQ_H * r + 2)
            root.blit(pygame.image.load(IMAGE_DIR + img), (x, y))

    if r1 > -1 and set.is_chessman(r1, c1):
        for m in set.board[r1][c1].valid_moves:
            x = int(SQ_W * m[1])
            y = int(SQ_H * m[0])
            root.blit(pygame.image.load(IMAGE_DIR + 'allowed_move.png'), (x, y))

    pygame.display.update()

def get_board_index(pos):
    c = int(pos[0]/SQ_W)
    r = int(pos[1]/SQ_H)
    return (r, c)

def make_move(set, event_pos, r1, c1):
    if (r1, c1) == (-1, -1):
        r, c = get_board_index(event_pos)
        if set.is_players_piece(r, c, set.who_plays):
            print(set.board[r][c].valid_moves)
            return r, c
        else:
            print('Please pick a valid piece. Look at caption to see which color plays.')
            return -1, -1
    else:
        r2, c2 = get_board_index(event_pos)
        if [r2, c2] in set.board[r1][c1].valid_moves:
            set.make_move(r1, c1, r2, c2)
        else:
            print('Invalid Move')

        r1, c1 = -1, -1

    return r1, c1



IMAGE_DIR = './images/'
BG_IMAGE = 'chessboard.png'
APP_WIDTH, APP_HEIGHT = (800, 800)
SQ_W = int(APP_WIDTH/8)
SQ_H = int(APP_HEIGHT/8)

PLAYER = 'b' # Players plays black. Need to change display mechanics to allow player to face blacks

if __name__=='__main__':
    main()
