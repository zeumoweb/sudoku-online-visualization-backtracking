from flask import Flask, render_template, url_for, redirect, request, jsonify
import game
import solve

app = Flask(__name__)

b = [
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
# c = [1,0,0,0,0,2,4,8,0,9,4,0,8,0,0,7,5,0,0,2,0,0,0,0,0,0,0,0,0,0,0,9,6,5,0,0,3,0,7,0,8,4,6,9,1,6,0,0,0,5,0,0,0,8,0,8,0,0,6,0,0,2,0,0,0,9,4,1,5,8,7,3,4,0,3,0,0,8,0,6,5]
# b = []
# for i in range(9):
#     t = []
#     for j in range(9):
#         t.append(c[i*9 +j])
#     b.append(t)


grid = game.Grid(b)
@app.route('/', methods = ['GET', 'POST'])
def index():
    global b, grid

    if request.method  == "GET":
        print("öppps run again")
        return render_template('index.html', board=grid.userBoard)

    if request.method == "POST":
        result = request.get_json() # take data passed by the user
        if  grid.cells[result["row"]][result["col"]].editable and not grid.solved:   # check if cell is editable
            valid = solve.isValid(grid.userBoard, int(result["val"]), (int(result["row"]), int(result["col"])))
            grid.updateCell(int(result["val"]), int(result["row"]), int(result["col"]), solved = valid)
            cellsStatus = grid.cellsStatus()
            listOfEditable = grid.listOfEditable()
            return jsonify({
                "val": result['val'], 
                "isValid": valid, 
                "row": result["row"], 
                "col": result["col"],
                "editable": True, 
                "solved": grid.solved,
                "cellsStatus": cellsStatus,
                "listOfEditable": listOfEditable
                })
        if grid.solved:
            cellsStatus = grid.cellsStatus()
            listOfEditable = grid.listOfEditable()
            return jsonify({
                "solved": grid.solved,
                "cellsStatus": cellsStatus,
                "listOfEditable": listOfEditable
            })
        # grid.displayBoard()
        fixed_value = grid.cells[result["row"]][result["col"]].value
        print('heloo..........')
        return jsonify({
            "val" : fixed_value,
            "isValid": True, 
            "row": result["row"], 
            "col": result["col"],
            "editable": False,
            "solved": grid.solved 
            })


@app.route('/solve', methods = ["GET", "POST"])
def cal():
    global grid
    if grid.solved:
        return jsonify(False)
    solved_board =  solve.Solve(grid.cleanBoard)
    print(solved_board[0])
    return jsonify(solved_board[1])

@app.route("/complete")
def complete():
    print('niovbuojopjeiovfuij')
    print(grid.solved)
    return render_template("base.html")

if __name__ == "__main__":
    app.run(debug=True)


