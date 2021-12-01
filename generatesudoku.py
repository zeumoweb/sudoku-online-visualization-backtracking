'''
In this file, we will write the algorithm to randomly create a sudoku board based
'''
import copy
import random
# create a sudoku board fill with zeros
board = [[0 for i in range(9)] for j in range(9)]
# print(board)

''' 
    Just as  with the solving algorithm, we will use backtracking to generate an already
     solved board and we will later randomly delete part of the cells to generate our puzzle.
'''
class Sudoku:

    def __init__(self):
        self.count = 0
        self.board = [[0 for i in range(9)] for j in range(9)] # create a sudoku board fill with zeros
        self.animationPath = []
        self.level = "Medium"

    def isValid(self, board, num, pos):
        ''' Check if putting a value in a given cell is valid '''
        row_index = pos[0]
        col_index = pos[1]
        for i in range(len(board[0])):

            # check if number appears in row
            if board[row_index][i] == num and i != col_index:
                return False

            # check if number appears in column
            if board[i][col_index] == num and i != row_index:
                return False
            
            # check if number appears in 3x3 box
        box_x = pos[0]//3
        box_y = pos[1]//3
        for i in range(box_x*3, box_x*3 + 3):
            for j in range(box_y*3, box_y*3 + 3):
                if board[i][j] == num and i != row_index and j != col_index:
                    return False
        return True


    def find_empty_cell(self, board):
        ''' find the first empty cell and return its location'''
        for row_index in range(9):
            for col_index in range(9):
                if board[row_index][col_index] == 0:
                    return (row_index, col_index)
        return False


    def generate_solved_board(self, board):
     """ generates a fully solved sudoku board with backtracking """
     nums = [1,2,3,4,5,6,7,8,9]
     for i in range(81):
        row=i//9
        col=i%9
        #find next empty cell
        if board[row][col]==0:
            random.shuffle(nums)      
            for number in nums:
                if self.isValid(board, number, (row, col)):
                    board[row][col]=number
                    if not self.find_empty_cell(board):
                        return True
                    else:
                        if self.generate_solved_board(board):
                            return True
            break
     board[row][col]=0  
     return False

    def solve_puzzle(self, board):
        ''' Another version of the sudoku solving algorithm that will keep track of the number of possible soltion that can exist for a given puzzle '''
        for i in range(81):
            row = i // 9
            col = i % 9
            # look for the next empty cell
            if board[row][col] == 0:
                for num in range(1, 10):
                    if self.isValid(board, num, (row, col)):
                        board[row][col] = num
                        if not self.find_empty_cell(board):
                            self.count += 1
                            break
                        else:
                            if self.solve_puzzle(board):
                                return True 
                break
        board[row][col] = 0
        return False

    def get_non_empty_cells(self, board):
        ''' function to return a list of positions of non-empty cells '''
        arr = []
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    arr.append((i, j))
        random.shuffle(arr)
        return arr


    def genPuzzle(self):
        '''
        Create puzzle by randomly removing numbers from the grid and making sure that the solution is still unique
        boards with more than 17 empty cells can have more than one solution.
        Generate the perfect puzzle

        '''
        self.generate_solved_board(self.board)
        non_empty_cells = self.get_non_empty_cells(self.board)
        num_non_empty_cells = len(non_empty_cells)
        if self.level == "Beginner":
            rounds = 30
        elif self.level == "Easy":
            rounds = 37
        elif self.level == "Medium":
            rounds = 43
        elif self.level == "Hard":
            rounds = 45
        elif self.level == "Difficult":
            rounds = 50
        elif self.level == "Evil":
            rounds = 51
        while rounds > 0 and num_non_empty_cells >= 17:
            #there should be at least 17 clues
            row,col = non_empty_cells.pop()
            num_non_empty_cells -= 1
            # We will add the cell value back if there is more than one solution when that cell is removed
            removed_cell = self.board[row][col]
            self.board[row][col]=0
            #make a copy of the grid to solve
            grid_copy = copy.deepcopy(self.board)
            self.solve_puzzle(grid_copy)   
            #if there is more than one solution, put the last removed cell back into the grid
            if self.count != 1:
                board[row][col] = removed_cell
                num_non_empty_cells += 1
                rounds -=1
        return self.board


    
    def Solve(self, board):
        if not self.find_empty_cell(board):
            return board, self.animationPath
        else:
            row, col = self.find_empty_cell(board)
            for i in range(1, 10):
                if self.isValid(board, i, (row, col)):
                    self.animationPath.append((i, row, col))
                    board[row][col] = i
                    # animation.append((i, row, col))
                    if self.Solve(board):
                        return board, self.animationPath
                    self.animationPath.append((0, row, col))
                    board[row][col] = 0


    def display_board(self, board):
        for i in range(len(board)):
            if i%3 == 0 and i != 0:
                print('-------------------')
            for j in range(len(board[0])):
                if j%3 == 0 and j != 0:
                    print('|', end='')
                if j != 9:
                    print(str(board[i][j]) + ' ', end='')
            print()





    


