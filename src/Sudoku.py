from flask import Flask, render_template, request

from src import logic

app = Flask(__name__)


@app.route("/sudoku")
def random_sudoku():
    board = logic.generate_board()
    initial_board = [[value for value in row] for row in board]
    logic.solve(board=board)
    return render_template("sudoku.html", initial_board=initial_board, solved_board=board)


@app.route("/sudoku", methods=['POST'])
def check_random_sudoku():
    # Prepares a initial and solved boards from original initial board
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

    # Prepares a filled board from user input
    values = request.form.getlist('value')
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
            if values[row * 9 + col] != '':
                filled_board[row][col] = int(values[row * 9 + col])
            else:
                is_board_full = False
    if not logic.check_if_board_is_valid(filled_board):
        return render_template("sudoku_checked_invalid.html", initial_board=initial_board, filled_board=filled_board,
                               solved_board=board)
    elif is_board_full:
        return render_template("sudoku_checked_completed.html", initial_board=initial_board, filled_board=filled_board)
    else:
        # Solve current state of the sudoku board (after user input)
        board = [[value for value in row] for row in filled_board]
        logic.solve(board=board)
        # Is solution is not found (recursive algorithm returned the same board as input) return invalid solution page
        if board == filled_board:
            board = [[value for value in row] for row in initial_board]
            logic.solve(board=board)
            return render_template("sudoku_checked_invalid.html", initial_board=initial_board,
                                   filled_board=filled_board,
                                   solved_board=board)
        else:
            return render_template("sudoku_checked_correct.html", initial_board=initial_board,
                                   filled_board=filled_board,
                                   solved_board=board)


@app.route('/sudoku/solve/')
def input_board_to_solve():
    initial_board = [
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
    return render_template("solve_input.html", initial_board=initial_board)


@app.route('/sudoku/solve/', methods=['POST'])
def output_solved_board():
    # Prepares an initial board from user input
    values = request.form.getlist('value')
    initial_board = [
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
            if values[row * 9 + col] != '':
                initial_board[row][col] = int(values[row * 9 + col])
            else:
                is_board_full = False
    if not logic.check_if_board_is_valid(initial_board):
        return render_template("solve_invalid.html", initial_board=initial_board)
    board = [[value for value in row] for row in initial_board]
    logic.solve(board=board)
    for row in board:
        for value in row:
            if value == 0:
                return render_template("solve_invalid.html", initial_board=initial_board)
    if is_board_full:
        return render_template("solve_completed.html", initial_board=board)
    else:
        return render_template("solve_output.html", initial_board=initial_board, solved_board=board)


if __name__ == "__main__":
    app.run()
