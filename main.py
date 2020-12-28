import pygame
import time
import chess_set
import chess_player
import chessman

def main():
    set = chess_set.ChessSet()
    white = chess_player.ChessPlayer(set, 'w')
    black = chess_player.ChessPlayer(set, 'b')

    root = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess Game')
    bg = pygame.image.load(IMAGE_DIR + BG_IMAGE)

    whos_turn = 'w'
    r1, c1 = (-1, -1)

    running = True

    while running:
        update_display(root, bg, set, whos_turn)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if (r1, c1) == (-1, -1):
                    r1, c1 = get_board_index(event.pos)
                    if not set.is_chessman(r1, c1):
                        r1, c1 = -1, -1
                        print('Please select a piece in order to move it!')
                    else:
                        color = set.board[r1][c1].color
                        if not color == whos_turn:
                            print(f'Wrong team! Look at caption to see who''s turn it is.')
                            r1, c1 = -1, -1
                else:
                    r2, c2 = get_board_index(event.pos)
                    if set.is_chessman(r2, c2):
                        color = set.board[r2][c2].color
                    else:
                        color = ''

                    if not (r1, c1) == (r2, c2) and not color == whos_turn:
                        set.move(r1, c1, r2, c2)
                        if whos_turn == 'w':
                            whos_turn = 'b'
                        else:
                            whos_turn = 'w'
                    else:
                        print('Canceled move')
                    r1, c1 = -1, -1


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
                x = int(SQ_G*c + 2)
                y = int(SQ_H*r + 2)
                root.blit(pygame.image.load(IMAGE_DIR + img), (x, y))

    pygame.display.update()

def get_board_index(pos):
    c = int(pos[0]/SQ_G)
    r = int(pos[1]/SQ_H)
    return (r, c)

IMAGE_DIR = './images/'
BG_IMAGE = 'chessboard.png'
WIDTH, HEIGHT = (800, 800)
SQ_G = int(WIDTH/8)
SQ_H = int(HEIGHT/8)

if __name__=='__main__':
    main()
