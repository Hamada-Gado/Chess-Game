from .board import Board
from .constants import BLACK, COLS, ROWS, WHITE

def _check_up(board, col, color, up, stop=-1):
    checks = {}
    iUp = up

    while True:

        if up < 0 or stop == 0:
            break

        current = board[up][col]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "ROOK" or (iUp == up and current.name == "KING"):
                checks[(up, col)] = current
            break
        else:
            break
            
        up -= 1
        stop -= 1
    
    return checks

def _check_down(board, col, color, down, stop=-1):
    checks = {}
    iDown = down

    while True:

        if down >= ROWS or stop == 0:
            break

        current = board[down][col]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "ROOK" or (iDown == down and current.name == "KING"):
                checks[(down, col)] = current
            break
        else:
            break
            
        down += 1
        stop -= 1
    
    return checks

def _check_left(board, row, color, left, stop=-1):
    checks = {}
    iLeft = left

    while True:

        if left < 0 or stop == 0:
            break

        current = board[row][left]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "ROOK" or (iLeft == left and current.name == "KING"):
                checks[(row, left)] = current
            break
        else:
            break
            
        left -= 1
        stop -= 1
    
    return checks

def _check_right(board, row, color, right, stop=-1):
    checks = {}
    iRight = right

    while True:

        if right >= COLS or stop == 0:
            break

        current = board[row][right]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "ROOK" or (iRight == right and current.name == "KING"):
                checks[(row, right)] = current
            break
        else:
            break
            
        right += 1
        stop -= 1
    
    return checks

def _check_left_diagonal_up(board, start, stop, color, left):
    checks = {}
    iLeft = left

    for row in range(start, stop, -1):

        if left < 0:
            break

        current = board[row][left]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "BISHOP" or (iLeft == left and (current.name == "PAWN" or current.name == "KING")):
                checks[(row, left)] = current
            break
        else:
            break
            
        left -= 1
    
    return checks

def _check_right_diagonal_up(board, start, stop, color, right):
    checks = {}
    iRight = right

    for row in range(start, stop, -1):

        if right >= COLS:
            break

        current = board[row][right]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "BISHOP" or (iRight == right and (current.name == "PAWN" or current.name == "KING")):
                checks[(row, right)] = current
            break
        else:
            break
            
        right += 1
    
    return checks

def _check_left_diagonal_down(board, start, stop, color, left):
    checks = {}
    iLeft = left

    for row in range(start, stop):

        if left < 0:
            break

        current = board[row][left]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "BISHOP" or (iLeft == left and (current.name == "PAWN" or current.name == "KING")):
                checks[(row, left)] = current
            break
        else:
            break
            
        left -= 1
    
    return checks

def _check_right_diagonal_down(board, start, stop, color, right):
    checks = {}
    iRight = right

    for row in range(start, stop):

        if right >= COLS:
            break

        current = board[row][right]
        if current == 0:
            pass
        elif current.color != color:
            if current.name == "QUEEN" or current.name == "BISHOP" or (iRight == right and (current.name == "PAWN" or current.name == "KING")):
                checks[(row, right)] = current
            break
        else:
            break
            
        right += 1
    
    return checks
    
def _check_lShape(board, row, col, color):
    checks = {}
    
    i = 1
    j = 2

    while i < 3 and j > 0:

        r = row-j
        c = col-i
        if r >= 0 and c >= 0:
            current = board[r][c]
            if current == 0:
                pass
            elif current.color != color and current.name == "KNIGHT":
                checks[(r, c)] = current
        
        r = row+j
        c = col+i
        if r < ROWS and c < COLS:
            current = board[r][c]
            if current == 0:
                pass
            elif current.color != color and current.name == "KNIGHT":
                checks[(r, c)] = current

        r = row-j
        c = col+i
        if r >= 0 and c < COLS:
            current = board[r][c]
            if current == 0:
                pass
            elif current.color != color and current.name == "KNIGHT":
                checks[(r, c)] = current
        
        r = row+j
        c = col-i 
        if r < ROWS and c >= 0:
            current = board[r][c]
            if current == 0:
                pass
            elif current.color != color and current.name == "KNIGHT":
                checks[(r, c)] = current

        i += 1
        j -= 1

    return checks

def inCheck(board: Board, color):
    checks = {}
    king = board.getKing(color)

    row = king.row
    col = king.col

    up = row-1
    down = row+1
    left = col-1
    right = col+1

    checks.update(_check_up(board.board, col, color, up))
    checks.update(_check_down(board.board, col, color, down))
    checks.update(_check_left(board.board, row, color, left))
    checks.update(_check_right(board.board, row, color, right))
    checks.update(_check_left_diagonal_up(board.board, up, -1, color, left))
    checks.update(_check_right_diagonal_up(board.board, up, -1, color, right))
    checks.update(_check_left_diagonal_down(board.board, down, ROWS, color, left))
    checks.update(_check_right_diagonal_down(board.board, down, ROWS, color, right))
    checks.update(_check_lShape(board.board, row, col, color))

    if checks: return True
    return False

def notPossible(temp_board: Board, piece, move, capture, color):
    piece = temp_board.getPiece(piece.row, piece.col)
    if capture:
        capture = temp_board.getPiece(capture.row, capture.col)
    new_board = stimulateMove(temp_board, piece, move, capture)
    return inCheck(new_board, color)

def stimulateMove(board: Board, piece, move, capture):
    if capture:
        board.remove(capture)
    board.move(piece, move[0], move[1])
        
    return board

