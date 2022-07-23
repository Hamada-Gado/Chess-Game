import pygame
pygame.font.init()

# game constants
WIDTH, HEIGHT = 720, 720
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
OFF_WHITE = (248, 240, 227)
BROWN_WOOD = (129, 84, 56)
CRYSTAL_BLUE = (94, 169, 190)
GREY = (128, 128, 128)
DARK_GREY = (59, 59, 59)
MELON = (243, 191, 179)
BLUE = (0, 0, 255)

# font
STATE_FONT = pygame.font.SysFont("comicsans", 40)

# icon
ICON = pygame.image.load("assets/icon.png")

# pieces
B_ROOK = pygame.image.load("assets/Chess_rdt60.png")
W_ROOK = pygame.image.load("assets/Chess_rlt60.png")
B_KNIGHT = pygame.image.load("assets/Chess_ndt60.png")
W_KNIGHT = pygame.image.load("assets/Chess_nlt60.png")
B_BISHOP = pygame.image.load("assets/Chess_bdt60.png")
W_BISHOP = pygame.image.load("assets/Chess_blt60.png")
B_KING = pygame.image.load("assets/Chess_kdt60.png")
W_KING = pygame.image.load("assets/Chess_klt60.png")
B_QUEEN = pygame.image.load("assets/Chess_qdt60.png")
W_QUEEN = pygame.image.load("assets/Chess_qlt60.png")
B_PAWN = pygame.image.load("assets/Chess_pdt60.png")
W_PAWN = pygame.image.load("assets/Chess_plt60.png")

ALL_PIECES = [B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_PAWN, W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_PAWN]

ENDGAME_BACKGROUND = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 40, 300, 80)

