from flask import Flask, render_template

import logic

app = Flask(__name__)


@app.route("/")
def sudoku():
    board = logic.generate_board()
    initial_board = [[value for value in row] for row in board]
    logic.solve(board=board)
    solved_board = [[value for value in row] for row in board]
    return render_template("index.html", initial_board=initial_board, solved_board=solved_board)


if __name__ == "__main__":
    app.run()
