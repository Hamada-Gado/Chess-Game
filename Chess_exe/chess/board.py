import pygame
from .piece import Piece
from .constants import ALL_PIECES, BLACK, CRYSTAL_BLUE, BROWN_WOOD, COLS, GREY, ROWS, SQUARE_SIZE, OFF_WHITE, WHITE

class Board:
    PADDING = 5
    OUTER_RADIUS = SQUARE_SIZE//2 - 5
    INNER_RADIUS = OUTER_RADIUS - 8

    def __init__(self):
        self.board = []
        self.choices = []
        self.lastMoved = 0
        self.createBoard()
        self.createChoices()

    def copy(self):
        copyObj = Board()
        i = 0
        for row in range(len(copyObj.board)):
            for col in range(len(copyObj.board)):
                piece = self.getPiece(row, col)
                if piece != 0:
                    copyObj.board[row][col] = piece.copy()
                else: copyObj.board[row][col] = 0
                
        return copyObj

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    if col == 0 or col == COLS-1:
                        self.board[row].append(Piece("ROOK", BLACK, row, col, ALL_PIECES[0]))
                    elif col == 1 or col == COLS-2:
                        self.board[row].append(Piece("KNIGHT", BLACK, row, col, ALL_PIECES[1]))
                    elif col == 2 or col == COLS-3:
                        self.board[row].append(Piece("BISHOP", BLACK, row, col, ALL_PIECES[2]))
                    elif col == 3:
                        self.board[row].append(Piece("QUEEN", BLACK, row, col, ALL_PIECES[3]))
                    elif col == 4:
                        self.board[row].append(Piece("KING", BLACK, row, col, ALL_PIECES[4]))
                elif row == 1:
                        self.board[row].append(Piece("PAWN", BLACK, row, col, ALL_PIECES[5]))
                elif row == ROWS-1:
                    if col == 0 or col == COLS-1:
                        self.board[row].append(Piece("ROOK", WHITE, row, col, ALL_PIECES[6]))
                    elif col == 1 or col == COLS-2:
                        self.board[row].append(Piece("KNIGHT", WHITE, row, col, ALL_PIECES[7]))
                    elif col == 2 or col == COLS-3:
                        self.board[row].append(Piece("BISHOP", WHITE, row, col, ALL_PIECES[8]))
                    elif col == 3:
                        self.board[row].append(Piece("QUEEN", WHITE, row, col, ALL_PIECES[9]))
                    elif col == 4:
                        self.board[row].append(Piece("KING", WHITE, row, col, ALL_PIECES[10]))
                elif row == ROWS-2:
                        self.board[row].append(Piece("PAWN", WHITE, row, col, ALL_PIECES[11]))
                else:
                    self.board[row].append(0)

    def createChoices(self):
        self.choices.append([])
        self.choices[0].append(Piece("ROOK", BLACK, 0, 0, ALL_PIECES[0]))
        self.choices[0].append(Piece("KNIGHT", BLACK, 0, 0, ALL_PIECES[1]))
        self.choices[0].append(Piece("BISHOP", BLACK, 0, 0, ALL_PIECES[2]))
        self.choices[0].append(Piece("QUEEN", BLACK, 0, 0, ALL_PIECES[3]))

        self.choices.append([])
        self.choices[1].append(Piece("ROOK", WHITE, 0, 0, ALL_PIECES[6]))
        self.choices[1].append(Piece("KNIGHT", WHITE, 0, 0, ALL_PIECES[7]))
        self.choices[1].append(Piece("BISHOP", WHITE, 0, 0, ALL_PIECES[8]))
        self.choices[1].append(Piece("QUEEN", WHITE, 0, 0, ALL_PIECES[9]))

    def updateChoicesPos(self, row, col, color):
        if color == BLACK: i = 0
        else: i = 1
        for piece in self.choices[i]:
            piece.move(row, col)
            row = row+1 if color == WHITE else row-1

    def drawSquares(self, win: pygame.Surface):
        win.fill(BROWN_WOOD)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, OFF_WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawDotes(self, win: pygame.Surface, row, col):
        center = (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2)
        pygame.draw.circle(win, GREY, center, 10)

    def drawCircle(self, win: pygame.Surface, piece: Piece):
        center = (piece.x + piece.image.get_width()//2, piece.y + piece.image.get_height()//2)
        pygame.draw.circle(win, GREY, center, self.OUTER_RADIUS)
        if piece.col in range(piece.row%2, ROWS, 2): color = OFF_WHITE
        else: color = BROWN_WOOD
        pygame.draw.circle(win, color, center, self.INNER_RADIUS)
        self.drawPiece(win, piece)

    def drawPiece(self, win: pygame.Surface, piece: Piece):
        win.blit(piece.image, (piece.x, piece.y))

    def drawChoices(self, win: pygame.Surface, row, col, color):
        if color == BLACK: i = 0
        else: i = 1
        x = col*SQUARE_SIZE
        y = (row-3)*SQUARE_SIZE if row != 0 else row
        background_boarder = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE*4)
        x += self.PADDING
        y += self.PADDING
        background = pygame.Rect(x, y, SQUARE_SIZE-self.PADDING*2, SQUARE_SIZE*4 - self.PADDING*2)
        pygame.draw.rect(win, GREY, background_boarder)
        pygame.draw.rect(win, CRYSTAL_BLUE, background)
        self.updateChoicesPos(row, col, color)
        for piece in self.choices[i]:
            if piece.color == color:
                self.drawPiece(win, piece)

    def drawBoard(self, win: pygame.Surface):
        self.drawSquares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    self.drawPiece(win, piece)

    def move(self, piece: Piece, row, col):
        if piece != 0:    
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
            piece.move(row, col)
            if piece.name == "KING" and piece.moveLen[0] == 2:
                rPiece = self.board[row][0]
                self.move(rPiece, row, 3)
            elif piece.name == "KING" and piece.moveLen[0] == -2:
                rPiece = self.board[row][7]
                self.move(rPiece, row, 5)

    def getPromotionPiece(self, row, col, color):
        if color == BLACK: i = 0
        else: i = 1
        for piece in self.choices[i]:
            if piece.row == row and piece.col == col:
                return piece
        return 0

    def getPiece(self, row, col) -> Piece:
        return self.board[row][col]

    def getKing(self, color) -> Piece:
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.name == "KING" and piece.color == color:
                    return piece

    def remove(self, piece: Piece):
        self.board[piece.row][piece.col] = 0

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_all_validMoves(self, pieces):
        moves = {}
        for piece in pieces:
            moves.update(self.getValidMoves(piece))
        return moves

    def check_promotions(self, color) -> Piece:
        if color == WHITE:
            for piece in self.board[0]:
                if piece != 0 and piece.name == "PAWN" and piece.color == color:
                    return piece

        else:
            for piece in self.board[7]:
                if piece != 0 and piece.name == "PAWN" and piece.color == color:
                    return piece

        return 0

    def getValidMoves(self, piece: Piece):
        from .checkMate import notPossible

        moves = {}

        row = piece.row
        col = piece.col
        color = piece.color

        up = row-1
        down = row+1
        left = col-1
        right = col+1

        if piece.name == "PAWN":
            if color == WHITE:
                if piece.moved == 0:
                    moves.update(self._traverse_up(col, color, up, 2))
                else:
                    moves.update(self._traverse_up(col, color, up, 1))
                moves.update(self._traverse_left_diagonal_up(up, max(up-1, -1), color, left))
                moves.update(self._traverse_right_diagonal_up(up, max(up-1, -1), color, right))
            else:
                if piece.moved == 0:
                    moves.update(self._traverse_down(col, color, down, 2))
                else:
                    moves.update(self._traverse_down(col, color, down, 1))
                moves.update(self._traverse_left_diagonal_down(down, min(down+1, ROWS), color, left))
                moves.update(self._traverse_right_diagonal_down(down, min(down+1, ROWS), color, right))
            moves.update(self._check_en_passant(row, col, color))
            
            for move in list(moves.keys()):
                r, c = move
                if c > col or c < col:
                    if moves[move] == 0:
                        moves.pop(move)
                if r != row and c == col:
                    if moves[move] != 0:
                        moves.pop(move)

            

        elif piece.name == "KING":
            moves.update(self._check_castling(piece, row, col, color))
            moves.update(self._traverse_up(col, color, up, 1))
            moves.update(self._traverse_down(col, color, down, 1))
            moves.update(self._traverse_left(row, color, left, 1))
            moves.update(self._traverse_right(row, color, right, 1))
            moves.update(self._traverse_left_diagonal_up(up, max(up-1, -1), color, left))
            moves.update(self._traverse_right_diagonal_up(up, max(up-1, -1), color, right))
            moves.update(self._traverse_left_diagonal_down(down, min(down+1, ROWS), color, left))
            moves.update(self._traverse_right_diagonal_down(down, min(down+1, ROWS), color, right))

        elif piece.name == "QUEEN":
            moves.update(self._traverse_up(col, color, up))
            moves.update(self._traverse_down(col, color, down))
            moves.update(self._traverse_left(row, color, left))
            moves.update(self._traverse_right(row, color, right))
            moves.update(self._traverse_left_diagonal_up(up, -1, color, left))
            moves.update(self._traverse_right_diagonal_up(up, -1, color, right))
            moves.update(self._traverse_left_diagonal_down(down, ROWS, color, left))
            moves.update(self._traverse_right_diagonal_down(down, ROWS, color, right))

        elif piece.name == "ROOK":
            moves.update(self._traverse_up(col, color, up))
            moves.update(self._traverse_down(col, color, down))
            moves.update(self._traverse_left(row, color, left))
            moves.update(self._traverse_right(row, color, right))

        elif piece.name == "BISHOP":
            moves.update(self._traverse_left_diagonal_up(up, -1, color, left))
            moves.update(self._traverse_right_diagonal_up(up, -1, color, right))
            moves.update(self._traverse_left_diagonal_down(down, ROWS, color, left))
            moves.update(self._traverse_right_diagonal_down(down, ROWS, color, right))

        elif piece.name == "KNIGHT":
            moves.update(self._traverse_lShape(row, col, color))

        for move in list(moves.keys()):
            if notPossible(self.copy(), piece, move, moves[move], color):
                moves.pop(move)

        return moves

    def _traverse_up(self, col, color, up, stop=-1):
        moves = {}

        while True:

            if up < 0 or stop == 0:
                break

            current = self.board[up][col]
            if current == 0:
                moves[(up, col)] = current
            elif current.color != color:
                moves[(up, col)] = current
                break
            else:
                break
                
            up -= 1
            stop -= 1
        return moves

    def _traverse_down(self, col, color, down, stop=-1):
        moves = {}

        while True:

            if down >= ROWS or stop == 0:
                break

            current = self.board[down][col]
            if current == 0:
                moves[(down, col)] = current
            elif current.color != color:
                moves[(down, col)] = current
                break
            else:
                break
                
            down += 1
            stop -= 1
        
        return moves

    def _traverse_left(self, row, color, left, stop=-1):
        moves = {}

        while True:

            if left < 0 or stop == 0:
                break

            current = self.board[row][left]
            if current == 0:
                moves[(row, left)] = current
            elif current.color != color:
                moves[(row, left)] = current
                break
            else:
                break
                
            left -= 1
            stop -= 1

        return moves

    def _traverse_right(self, row, color, right, stop=-1):
        moves = {}

        while True:

            if right >= COLS or stop == 0:
                break

            current = self.board[row][right]
            if current == 0:
                moves[(row, right)] = current
            elif current.color != color:
                moves[(row, right)] = current
                break
            else:
                break
                
            right += 1
            stop -= 1
        
        return moves

    def _traverse_left_diagonal_up(self, start, stop, color, left):
        moves = {}

        for row in range(start, stop, -1):

            if left < 0:
                break

            current = self.board[row][left]
            if current == 0:
                moves[(row, left)] = current
            elif current.color != color:
                moves[(row, left)] = current
                break
            else:
                break
                
            left -= 1
        
        return moves

    def _traverse_right_diagonal_up(self, start, stop, color, right):
        moves = {}

        for row in range(start, stop, -1):

            if right >= COLS:
                break

            current = self.board[row][right]
            if current == 0:
                moves[(row, right)] = current
            elif current.color != color:
                moves[(row, right)] = current
                break
            else:
                break
                
            right += 1
        
        return moves

    def _traverse_left_diagonal_down(self, start, stop, color, left):
        moves = {}

        for row in range(start, stop):

            if left < 0:
                break

            current = self.board[row][left]
            if current == 0:
                moves[(row, left)] = current
            elif current.color != color:
                moves[(row, left)] = current
                break
            else:
                break
                
            left -= 1
        
        return moves

    def _traverse_right_diagonal_down(self, start, stop, color, right):
        moves = {}

        for row in range(start, stop):

            if right >= COLS:
                break

            current = self.board[row][right]
            if current == 0:
                moves[(row, right)] = current
            elif current.color != color:
                moves[(row, right)] = current
                break
            else:
                break
                
            right += 1
        
        return moves
        
    def _traverse_lShape(self, row, col, color):
        moves = {}
        
        i = 1
        j = 2

        while i < 3 and j > 0:

            r = row-j
            c = col-i
            if r >= 0 and c >= 0:
                current = self.board[r][c]
                if current == 0:
                    moves[(r, c)] = current
                elif current.color != color:
                    moves[(r, c)] = current
            
            r = row+j
            c = col+i
            if r < ROWS and c < COLS:
                current = self.board[r][c]
                if current == 0:
                    moves[(r, c)] = current
                elif current.color != color:
                    moves[(r, c)] = current

            r = row-j
            c = col+i
            if r >= 0 and c < COLS:
                current = self.board[r][c]
                if current == 0:
                    moves[(r, c)] = current
                elif current.color != color:
                    moves[(r, c)] = current
            
            r = row+j
            c = col-i 
            if r < ROWS and c >= 0:
                current = self.board[r][c]
                if current == 0:
                    moves[(r, c)] = current
                elif current.color != color:
                    moves[(r, c)] = current

            i += 1
            j -= 1

        return moves

    def _check_en_passant(self, row, col, color):
        moves = {}
        
        if col+1 < COLS:
            current = self.board[row][col+1]
            if current != 0 and self.lastMoved == current and abs(current.moveLen[1]) == 2 and current.name == "PAWN" and current.moved == 1 and current.color != color:
                if color == WHITE:
                    moves[(row-1, col+1)] = current
                else:
                    moves[(row+1, col+1)] = current
        
        if col-1 >= 0:
            current = self.board[row][col-1]
            if current != 0 and self.lastMoved == current and abs(current.moveLen[1]) == 2 and current.name == "PAWN" and current.moved == 1 and current.color != color:
                if color == WHITE:
                    moves[(row-1, col-1)] = current
                else:
                    moves[(row+1, col-1)] = current

        return moves

    def _check_castling(self, piece, row, col, color):
        from .checkMate import notPossible
        moves = {}
        king = self.board[row][col]

        if color == WHITE:
            rook1 = self.board[7][0]
            rook2 = self.board[7][7]

            if king.moved == 0:

                isEmpty = True
                for i in range(1, 4):
                    if self.board[7][i] != 0:
                        isEmpty = False
                if rook1 != 0 and rook1.moved == 0 and isEmpty:
                    if not notPossible(self.copy(), piece, (row, col-1),0,color):
                        moves[(7, 2)] = 0

                isEmpty = True
                for i in range(5, 7):
                    if self.board[7][i] != 0:
                        isEmpty = False
                if rook2 != 0 and rook2.moved == 0 and isEmpty: 
                    if not notPossible(self.copy(), piece, (row, col+1),0,color):
                        moves[(7, 6)] = 0


        else:
            rook1 = self.board[0][0]
            rook2 = self.board[0][7]

            if king.moved == 0:

                isEmpty = True
                for i in range(1, 4):
                    if self.board[0][i] != 0:
                        isEmpty = False
                if rook1 != 0 and rook1.moved == 0 and isEmpty:
                    if not notPossible(self.copy(), piece, (row, col-1),0,color):
                        moves[(0, 2)] = 0
                
                isEmpty = True
                for i in range(5, 7):
                    if self.board[0][i] != 0:
                        isEmpty = False
                if rook2 != 0 and rook2.moved == 0 and isEmpty:
                    if not notPossible(self.copy(), piece, (row, col+1),0,color):
                        moves[(0, 6)] = 0

        return moves

        

