import pygame
import sys
from time import time
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
    clock = pygame.time.Clock()
    game = Game(WIN)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    game.hints[game.turn] = not game.hints[game.turn]
                if game.winner and event.key == pygame.K_r:
                    game.reset()

            if event.type == pygame.MOUSEBUTTONDOWN and not game.winner:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    main()


if __name__ == "__main__":
    main()