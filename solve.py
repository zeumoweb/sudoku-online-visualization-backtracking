def display_board(board):
    for i in range(len(board)):
        if i%3 == 0 and i != 0:
            print('-------------------')
        for j in range(len(board[0])):
            if j%3 == 0 and j != 0:
                print('|', end='')
            if j != 9:
                print(str(board[i][j]) + ' ', end='')
        print()


def find_empty_cell(board):
    for row_index in range(len(board)):
        for col_index in range(len(board[0])):
            if board[row_index][col_index] == 0:
                return (row_index, col_index)
    return False


def isValid(board, num, pos):
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
animation = []
def Solve(board):
    global animation
    if not find_empty_cell(board):
        return board, animation
    else:
        row, col = find_empty_cell(board)
        for i in range(1, 10):
            if isValid(board, i, (row, col)):
                animation.append((i, row, col))
                board[row][col] = i
                # animation.append((i, row, col))
                if Solve(board):
                    return board, animation
                animation.append((0, row, col))
                board[row][col] = 0

c = [1,0,0,0,0,2,4,8,0,9,4,0,8,0,0,7,5,0,0,2,0,0,0,0,0,0,0,0,0,0,0,9,6,5,0,0,3,0,7,0,8,4,6,9,1,6,0,0,0,5,0,0,0,8,0,8,0,0,6,0,0,2,0,0,0,9,4,1,5,8,7,3,4,0,3,0,0,8,0,6,5]
b = []
for i in range(9):
    t = []
    for j in range(9):
        t.append(c[i*9 +j])
    b.append(t)

# b = [
#     [0,0,0,0,0,1,4,0,0],
#     [0,2,0,0,0,0,0,0,5],
#     [0,0,0,0,0,5,6,0,3],
#     [2,0,0,0,8,0,0,6,4],
#     [7,0,3,0,0,0,5,9,8],
#     [0,5,0,4,0,0,0,0,2],
#     [0,0,0,0,0,0,0,0,0],
#     [8,1,5,0,6,0,3,0,9],
#     [0,0,0,8,0,9,2,5,6]
# ]
if __name__ == "__main__":
    # print(isValid(b, 0, (0, 0)))
    print(Solve(b)[0])
#[[5, 8, 6, 9, 3, 1, 4, 2, 7], [3, 2, 4, 6, 7, 8, 9, 1, 5], [1, 7, 9, 2, 4, 5, 6, 8, 3], [2, 9, 1, 5, 8, 3, 7, 6, 4], [7, 4, 3, 1, 2, 6, 5, 9, 8], [6, 5, 8, 4, 9, 7, 1, 3, 2], [9, 6, 2, 3, 5, 4, 8, 7, 1], [8, 1, 5, 7, 6, 2, 3, 4, 9], [4, 3, 7, 8, 1, 9, 2, 5, 6]]