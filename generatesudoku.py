'''
In this file, we will write the algorithm to randomly create a sudoku board based
'''
import copy
import solve
import random
# create a sudoku board fill with zeros

board = [[0 for i in range(9)] for j in range(9)]
# print(board)

''' 
    Just as  with the solving algorithm, we will use backtracking to generate an already
     solved board and we will later randomly delete part of the cells to generate our puzzle.
'''


def shuffle(arr):
    new_arr = []
    while len(new_arr) != 9:
        num = random.randint(1, 10)
        if num in arr:
            new_arr.append(num)
            arr.remove(num)
    for i in new_arr:
        arr.append(i)

def generate_board(board):
     """generates a full solution with backtracking"""
     nums = [1,2,3,4,5,6,7,8,9]
     for i in range(81):
        row=i//9
        col=i%9
        #find next empty cell
        if board[row][col]==0:
            shuffle(nums)      
            for number in nums:
                if solve.isValid(board, number, (row, col)):
                    board[row][col]=number
                    if not solve.find_empty_cell(board):
                        return True
                    else:
                        if generate_board(board):
                            #if the grid is full
                            return True
            break
     board[row][col]=0  
     return False

# Create puzzle by randomly removing numbers from the grid and making sure that the solution is still unique
# boards with more than 17 empty cells can have more than one solution

# function to return a list of positions of non-empty cells

def get_non_empty_cells(self):
    arr = []
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                arr.append((i, j))
    return arr

# Generate the perfect puzzle

def genPuzzle(board):
    non_empty_cells = get_non_empty_cells(board)
    num_non_empty_cells = len(non_empty_cells)
    rounds = 3
    while rounds > 0 and num_non_empty_cells >= 17:
        #there should be at least 17 clues
        row,col = non_empty_cells.pop()
        num_non_empty_cells -= 1
        #might need to put the square value back if there is more than one solution
        removed_square = board[row][col]
        board[row][col]=0
        #make a copy of the grid to solve
        grid_copy = copy.deepcopy(board)
        #initialize solutions counter to zero
        counter=0      
        self.solve_puzzle(grid_copy)   
        #if there is more than one solution, put the last removed cell back into the grid
        if self.counter!=1:
            board[row][col]=removed_square
            num_non_empty_cells += 1
            rounds -=1
    return



    


