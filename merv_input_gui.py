#input board gui
import pygame
import time


class Grid:
    #board = random_fn.random_inp()
    def __init__(self, board, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    
    def update_board(self, b):
        self.board = b
        self.cubes = [[Cube(self.board[i][j], i, j, self.width, self.height) for j in range(self.cols)] for i in range(self.rows)]
        self.update_model()

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None
    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            thick = 4 if i % 3 == 0 and i != 0 else 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set(val)
        self.update_model()

    def validate_board(self):
        if isValidSudoku(self.model):
            print("valid board")
            #call sudoko main
            return self.model
            
        else:
            print("invalid board")
            b_restart = [[0 for _ in range(9)] for _ in range(9)]
            self.update_board(b_restart)
            return None



class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
        
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)
    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def is_valid(grid, row, col, val):
    for i in range(9):
        if((grid[row][i] == val) or 
           (grid[i][col] == val) or 
           (grid[(3*(row//3) +(i//3))][(3*(col//3))+(i%3)] == val)):
            
            return False
    return True

def isValidSudoku(board):
    def is_valid_placement(board, num, row, col):
        # Check if the number is not in the same row or column
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False

        # Check if the number is not in the same 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve_sudoku(board):
        for i in range(81):
          row = i // 9
          col = i % 9
          cell_val = board[row][col]
          board[row][col] = 0   #to avoid considering the cell value when validating


          
          #early detection of invalid boards
          if cell_val != 0:
              if cell_val < 0 or cell_val >9:
                  return False
              if not is_valid(board, row, col ,cell_val):
                  return False
        
          board[row][col] = cell_val  #return board to its initial form after validation


        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid_placement(board, num, i, j):
                            board[i][j] = num
                            if solve_sudoku(board):
                                return True
                            board[i][j] = 0  # Backtrack if the current placement is not valid
                    return False  # No valid number found for this cell

        return True  # All cells filled successfully

    # Copy the board to avoid modifying the input
    board_copy = [row[:] for row in board]

    # Attempt to solve the Sudoku
    if solve_sudoku(board_copy):
        return True  # The board is valid
    else:
        return False  # No solution found, or the initial board is invalid

    

