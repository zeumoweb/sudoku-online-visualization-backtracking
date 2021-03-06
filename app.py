from flask import Flask, render_template, url_for, request, jsonify, redirect
import game
from generatesudoku import Sudoku
from datetime import datetime


app = Flask(__name__)

grid = 0

import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'statistics.txt')
print(my_file)
# track game data
startTime = 0
# Home route


@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")


# Play route
@app.route('/play/', defaults={'level': 'Medium'}, methods=['GET', 'POST'])
@app.route('/play/<level>', methods=['GET', 'POST'])
def play(level):
    global grid, startTime
    if request.method == "GET":
        sudoku = Sudoku()
        sudoku.level = level
        puzzle_board = sudoku.genPuzzle()
        grid = game.Grid(puzzle_board)
        startTime = datetime.now()
        return render_template('play.html', board=grid.userBoard, level=level)

    if request.method == "POST":
        result = request.get_json()  # take data passed by the user
        if "row" in result:
            # check if cell is editable
            if grid.cells[result["row"]][result["col"]].editable and not grid.solved:
                valid = Sudoku().isValid(grid.userBoard, int(
                    result["val"]), (int(result["row"]), int(result["col"])))
                grid.updateCell(int(result["val"]), int(
                    result["row"]), int(result["col"]), solved=valid)
                cellsStatus = grid.cellsStatus()
                listOfEditable = grid.listOfEditable()
                if grid.solved:
                    # storing the game statistics in a file
                    timeSpend = (datetime.now() - startTime).total_seconds()
                    save_data(my_file, timeSpend, level)

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
                    "listOfEditable": listOfEditable,
                    "val": result['val'],
                })
            fixed_value = grid.cells[result["row"]][result["col"]].value
            return jsonify({
                "val": fixed_value,
                "isValid": True,
                "row": result["row"],
                "col": result["col"],
                "editable": False,
                "solved": grid.solved
            })
        elif "level" in result:
            return jsonify(level=result["level"])


# Automatic solving route

@app.route('/solve', methods=["GET", "POST"])
def visualization():
    global grid
    if grid.solved:
        return jsonify(False)
    solved_board = Sudoku().Solve(grid.cleanBoard)
    return jsonify(solved_board[1])


@app.route("/info", methods=["POST", "GET"])
def info():
    with open(my_file, "r") as file:
        data = file.readlines()
        hour = float(data[0].strip())//(60*60)
        mins = float(data[0].strip())//(60) - hour*60
        easy = int(float(data[2].strip()))
        beg = int(float(data[1].strip()))
        med = int(float(data[3].strip()))
        hard = int(float(data[4].strip()))
        diff = int(float(data[5].strip()))
        evil = int(float(data[6].strip()))
        total = int(float(data[7].strip()))
    return render_template("info.html", hour=hour, mins=mins, easy=easy, beg=beg, med=med, hard=hard, diff=diff, evil=evil, total=total)


''' 
Storing game Statistics to a file
The first line in the file represent the total number of seconds spend playing the Game
The Second line represent the total number of times the level Beginner has been played
The third line represent the total number of times the level easy has been played
The fourth line represent the total number of times the level Medium has been played
The fifth line represent the total number of times the level Hard has been played
The sixth line represent the total number of times the level Difficult has been played
The seventh line represent the total number of times the level Evil has been played
The eigth line represent the total number of times the game was played
'''
b, e, m, h, d, e, total, total_time = 0, 0, 0, 0, 0, 0, 0, 0

def save_data(file, timeSpend=0, level="Medium"):
    global b, e, m, h, d, e, total
    with open(file, "r") as stats:
        data = stats.readlines()
        print(data)
        total_time = float(data[0].strip())
        b = float(data[1].strip())
        e = float(data[2].strip())
        m = float(data[3].strip())
        h = float(data[4].strip())
        d = float(data[5].strip())
        e = float(data[6].strip())
        total = float(data[7].strip())

    with open(file, "w") as data:
        data.write(str(timeSpend + total_time) + "\n")
        if level == "Beginner":
            b += 1
        elif level == "Easy":
            e += 1
        elif level == "Medium":
            m += 1
        elif level == "Hard":
            h += 1
        elif level == "Difficult":
            d += 1
        elif level == "Evil":
            e += 1
        total += 1
        arr = [b, e, m, h, d, e, total]
        print(arr)
        for i in arr:
            data.write(str(i) + '\n')


if __name__ == "__main__":
    app.run()
