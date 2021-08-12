from flask import Flask, render_template, request

import logic

app = Flask(__name__)


@app.route("/")
def random_sudoku():
    board = logic.generate_board()
    initial_board = [[value for value in row] for row in board]
    logic.solve(board=board)
    solved_board = [[value for value in row] for row in board]
    return render_template("sudoku.html", initial_board=initial_board, solved_board=solved_board)


@app.route("/", methods=['POST'])
def check_random_sudoku():
    starting_board = request.form.getlist('initial_board')
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    for row in range(9):
        for col in range(9):
            if starting_board[row * 9 + col] != '':
                board[row][col] = int(starting_board[row * 9 + col])
    initial_board = [[value for value in row] for row in board]
    logic.solve(board=board)
    solved_board = [[value for value in row] for row in board]

    text = request.form.getlist('value')
    filled_board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    is_board_full = True
    for row in range(9):
        for col in range(9):
            if text[row * 9 + col] != '':
                filled_board[row][col] = int(text[row * 9 + col])
            else:
                is_board_full = False
    if not logic.check_if_board_is_valid(filled_board):
        return render_template("sudoku_checked_invalid.html", initial_board=initial_board, filled_board=filled_board,
                               solved_board=solved_board)
    elif is_board_full:
        return render_template("sudoku_checked_completed.html", initial_board=initial_board, filled_board=filled_board)
    else:
        board = [[value for value in row] for row in filled_board]
        logic.solve(board=board)
        solved_board = [[value for value in row] for row in board]
        return render_template("sudoku_checked_correct.html", initial_board=initial_board, filled_board=filled_board,
                               solved_board=solved_board)


@app.route('/solve/')
def input_board_to_solve():
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    initial_board = [[value for value in row] for row in board]
    return render_template("solve_input.html", initial_board=initial_board)


@app.route('/solve/', methods=['POST'])
def output_solved_board():
    text = request.form.getlist('value')
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    is_board_full = True
    for row in range(9):
        for col in range(9):
            if text[row * 9 + col] != '':
                board[row][col] = int(text[row * 9 + col])
            else:
                is_board_full = False
    initial_board = [[value for value in row] for row in board]
    if not logic.check_if_board_is_valid(initial_board):
        return render_template("solve_invalid.html", initial_board=initial_board)
    logic.solve(board=board)
    solved_board = [[value for value in row] for row in board]
    if is_board_full:
        return render_template("solve_completed.html", initial_board=initial_board)
    else:
        return render_template("solve_output.html", initial_board=initial_board, solved_board=solved_board)


if __name__ == "__main__":
    app.run()
