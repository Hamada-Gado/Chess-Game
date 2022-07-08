import pygame
import sys
from chess.constants import ICON, SQUARE_SIZE, WIDTH, HEIGHT
from chess.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHESS")
pygame.display.set_icon(ICON)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    t = 333
    clock = pygame.time.Clock()
    game = Game(WIN)

    while t:
        clock.tick(FPS)

        if game.winner:
            t -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    main()


if __name__ == "__main__":
    main()