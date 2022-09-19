import pygame
from .constants import BLACK, ENDGAME_BACKGROUND, GREY, HEIGHT, MELON, STATE_FONT, WHITE, WIDTH
from .board import Board
from .checkMate import inCheck

class Game:

    def __init__(self, win: pygame.Surface):
        self.win = win
        self._init()

    def _init(self):
        self.board = Board()
        self.turn = WHITE
        self.selected = None
        self.promoting = 0
        self.winner = None
        self.state_text = None
        self.validMoves = {}
    
    def reset(self):
        self._init()

    def update(self):
        self.board.drawBoard(self.win)
        self.drawValidMoves(self.validMoves)
        if self.promoting:
            self.board.drawChoices(self.win, self.promoting.row, self.promoting.col, self.turn)
        if self.winner:
            pygame.draw.rect(self.win, MELON, ENDGAME_BACKGROUND)
            self.win.blit(self.state_text, (WIDTH//2 - self.state_text.get_width()//2, HEIGHT//2 - self.state_text.get_height()//2))
        else: self.state()
        pygame.display.update()

    def state(self):
        pieces = self.board.get_all_pieces(self.turn)
        moves = self.board.get_all_validMoves(pieces)
        if inCheck(self.board, self.turn) and not moves:
            self.changeTurn()
            self.winner = self.turn
            color = "WHITE" if self.turn == WHITE else "BLACK"
            self.state_text = STATE_FONT.render(color + " WON!!", 1, self.turn)

        elif not moves:
            self.winner = GREY
            self.state_text = STATE_FONT.render("STALEMATE!!", 1, GREY)
        else:
            self.winner = None
        

    def select(self, row, col):
        if self.selected:

            if self.promoting:
                result = self._promote()
            else:
                result = self._move(row, col)
            if not result:
                self.selected = None
                self.validMoves = {}
                self.select(row, col)

        if not self.promoting:
            piece = self.board.getPiece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.validMoves = self.board.getValidMoves(piece)
        else:
            if self.selected != 0 and self.selected.name == "PAWN": self.selected = 0
            else: self.selected = self.board.getPromotionPiece(row, col, self.turn)
            self.validMoves = {}
            self._promote()

    def _move(self, row, col):
        if self.selected and not self.promoting and (row, col) in self.validMoves:

            capture = self.validMoves[(row, col)]
            if capture:
                self.board.remove(capture)

            self.board.move(self.selected, row, col)
            self.board.lastMoved = self.selected
            self.promoting = self.board.check_promotions(self.turn)
            
            if not self.promoting:
                self.changeTurn()

            return True

        return False

    def _promote(self):
        if self.selected and self.promoting:
            self.promoting.promote(self.selected)
            self.promoting = 0
            self.changeTurn()
            return True
        return False

    def flipBoard(self):
        for i in range(len(self.board.board[:])//2):
            self.board.board[i], self.board.board[-1-i] = self.board.board[-1-i], self.board.board[i]
            for j in range(len(self.board.board[i][:])//2):
                piece1 = self.board.board[i][j]
                piece2 = self.board.board[i][-1-j]
                piece3 = self.board.board[-1-i][j]
                piece4 = self.board.board[-1-i][-1-j]
                if piece1 != 0:
                    piece1.row = len(self.board.board[i]) - 1 - piece1.row
                    piece1.col = len(self.board.board[i]) - 1 - piece1.col
                    piece1.calcPos()
                if piece2 != 0:
                    piece2.row = len(self.board.board[i]) - 1 - piece2.row
                    piece2.col = len(self.board.board[i]) - 1 - piece2.col
                    piece2.calcPos()
                if piece3 != 0:
                    piece3.row = len(self.board.board[i]) - 1 - piece3.row
                    piece3.col = len(self.board.board[i]) - 1 - piece3.col
                    piece3.calcPos()
                if piece4 != 0:
                    piece4.row = len(self.board.board[i]) - 1 - piece4.row
                    piece4.col = len(self.board.board[i]) - 1 - piece4.col
                    piece4.calcPos()
                self.board.board[i][j], self.board.board[i][-1-j] = self.board.board[i][-1-j], self.board.board[i][j]
                self.board.board[-1-i][j], self.board.board[-1-i][-1-j] = self.board.board[-1-i][-1-j], self.board.board[-1-i][j]

    def changeTurn(self):
        self.validMoves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        self.flipBoard()

    def drawValidMoves(self, moves):
        for move, capture in moves.items():
            row, col = move
            if not capture or capture.row != row:
                self.board.drawDotes(self.win, row, col)
            else:
                self.board.drawCircle(self.win, capture)

