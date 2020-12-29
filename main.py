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

    while running:
        update_display(root, bg, set, whos_turn)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                r1, c1, whos_turn = make_move(set, event.pos, whos_turn, r1, c1)

            if event.type == pygame.QUIT:
                running = False

    pygame.display.quit()

def update_display(root, bg, set, whos_turn, ):
    if whos_turn == 'w':
        caption = 'Whites to play'
    else:
        caption = 'Blacks to play'
    pygame.display.set_caption('Chess Game - ' + caption)
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
        if set.is_valid_piece(r, c, whos_turn):
            return r, c, whos_turn
        else:
            print('Please pick a valid piece. Look at caption to see which color plays.')
            return -1, -1, whos_turn
    else:
        r2, c2 = get_board_index(event_pos)
        if set.is_valid_move(r1, c1, r2, c2, whos_turn):
            set.move(r1, c1, r2, c2)
            if whos_turn == 'w':
                whos_turn = 'b'
            else:
                whos_turn = 'w'
        else:
            print('Invalid Move')

        r1, c1 = -1, -1

    return r1, c1, whos_turn



IMAGE_DIR = './images/'
BG_IMAGE = 'chessboard.png'
APP_WIDTH, APP_HEIGHT = (800, 800)
SQ_W = int(APP_WIDTH/8)
SQ_H = int(APP_HEIGHT/8)

if __name__=='__main__':
    main()
