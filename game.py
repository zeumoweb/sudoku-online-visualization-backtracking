

import time
from copy import deepcopy

import solve

board = [
    [0,0,0,0,0,1,4,0,0],
    [0,2,0,0,0,0,0,0,5],
    [0,0,0,0,0,5,6,0,3],
    [2,0,0,0,8,0,0,6,4],
    [7,0,3,0,0,0,5,9,8],
    [0,5,0,4,0,0,0,0,2],
    [0,0,0,0,0,0,0,0,0],
    [8,1,5,0,6,0,3,0,9],
    [0,0,0,8,0,9,2,5,6]
]



# Cell

class Cell:
    '''Initialize a cell object. A cell in sudoku puzzle represents each box that contains a number.
    There are 81 cells in total and cells are grouped in groups of 9 to form boxes.
    We will consider the boxes as having index 0 to 8 and a cell can fall in either of these boxes.
    
    answer : --> int
    position: --> tuple
    solved: --> boolean

     '''
    def __init__(self, row, col, value = 0, editable = True, solved = False):
        self.value = value
        self.row = row
        self.col = col
        self.solved = solved
        self.editable = editable

    def clear(self):
        ''' reset all the information of the cell'''
        if not self.solved:
            self.value = 0
            self.solved = False

    def setValue(self, val):
        ''' set the value of a particular cell '''
        if self.editable:
            self.value = val
      
# Grid

class Grid:
    '''
    Instantiating a grid object. This class will have all the properties
     and methods of the grid object.

    userBoard: Board that will be manipulated in the course of the game. --> list
    cleanBoard: Board that will be fed to the solve function. --> list
    isSolved: Bool representing the status of the game 
    '''
    def __init__(self, board):
        self.userBoard = board 
        self.cleanBoard = deepcopy(board) # This value won't change and will be used as input by the solve function
        self.cells = []
        self.solved = False
        for i in range(9):
            temp = []
            for j in range(9):
                if  self.userBoard[i][j] != 0:
                    temp.append(Cell(i, j, self.userBoard[i][j], False, True))
                else:
                    temp.append(Cell(i, j, self.userBoard[i][j]))
            self.cells.append(temp)

    def updateUserBoard(self):
        ''' updates the board with the information of the cells'''
        for i in range(9):
            for j in range(9):
                self.userBoard[i][j] = self.cells[i][j].value
    
    def updateCell(self, val, row, col, solved=True):
        ''' Update a cell object with a new value '''
        self.complete()
        if not self.solved:
            self.cells[row][col].setValue(val)
            self.cells[row][col].solved = solved
            self.updateUserBoard()
            self.complete()

    def updateCells(self):
        ''' Update the list of cells with a new list of cells object with values corresponding to values in the userBoard'''
        new_cells = []
        for i in range(9):
            temp = []
            for j in range(9):
                if  self.userBoard[i][j] != 0:
                    temp.append(Cell(i, j, self.userBoard[i][j], False))
                else:
                    temp.append(Cell(i, j, self.userBoard[i][j]))
            new_cells.append(temp)

        self.cells = new_cells

    def setSolved(self, bol):
        self.solved = bol

    def complete(self):
        ''' check is the grid has been completely filled with correct values '''
        for i in range(9):
            for j in range(9):
                if not solve.isValid(self.userBoard, self.userBoard[i][j], (i, j)) or self.userBoard[i][j] == 0:
                    self.solved = False
                    return
        self.solved = True
    
    def cellsStatus(self):
        ''' return a list that contains a boolean stating if a cell has a correct value or not'''
        arr = []
        for i in range(9):
            for j in range(9):
                arr.append(solve.isValid(self.userBoard, self.userBoard[i][j], (i, j)))
        return arr

    def listOfEditable(self):
        ''' Return List of Editable cells '''
        arr = []
        for i in range(9):
            for j in range(9):
                arr.append(self.cells[i][j].editable)
        return arr
        
    def displayBoard(self):
        for i in range(len(self.userBoard)):
            if i%3 == 0 and i != 0:
                print('-------------------')
            for j in range(len(self.userBoard[0])):
                if j%3 == 0 and j != 0:
                    print('|', end='')
                if j != 9:
                    print(str(self.userBoard[i][j]) + ' ', end='')
            print()

    

if __name__ == '__main__':
    g=  Grid(board)
    g.displayBoard()
    print("solved???", g.solved)
    print(g.userBoard)
    g.updateCell(5, 0, 0)
    print(g.userBoard)
    print("solved???",g.solved)