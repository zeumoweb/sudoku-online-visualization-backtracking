from flask import Flask, render_template, url_for, redirect, request, jsonify
import game
from generatesudoku import Sudoku

app = Flask(__name__)

# Home route
@app.route('/', methods=["POST", "GET"]) 
def index():
    return render_template("index.html")


grid = 0
# Play route
@app.route('/play', methods = ['GET', 'POST'])
def play():
    global grid
    if request.method  == "GET":
        puzzle_board = Sudoku().genPuzzle()
        grid = game.Grid(puzzle_board)
        return render_template('play.html', board=grid.userBoard)

    if request.method == "POST":
        result = request.get_json() # take data passed by the user
        if "row" in result:
            if  grid.cells[result["row"]][result["col"]].editable and not grid.solved:   # check if cell is editable
                valid = Sudoku().isValid(grid.userBoard, int(result["val"]), (int(result["row"]), int(result["col"])))
                grid.updateCell(int(result["val"]), int(result["row"]), int(result["col"]), solved = valid)
                cellsStatus = grid.cellsStatus()
                listOfEditable = grid.listOfEditable()
                # grid.displayBoard()
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
            fixed_value = grid.cells[result["row"]][result["col"]].value
            return jsonify({
                "val" : fixed_value,
                "isValid": True, 
                "row": result["row"], 
                "col": result["col"],
                "editable": False,
                "solved": grid.solved 
                })
        elif "level" in result:
            return jsonify(result ="result")
                
    


# Automatic solving route

@app.route('/solve', methods = ["GET", "POST"])
def cal():
    global grid
    if grid.solved:
        return jsonify(False)
    solved_board =  Sudoku().Solve(grid.cleanBoard)
    return jsonify(solved_board[1])


if __name__ == "__main__":
    app.run(debug=True)


