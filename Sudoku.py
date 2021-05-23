import json
import urllib.request
import random
from flask import Flask, render_template

initial_board_manual_input = False


def generate_board():
    if initial_board_manual_input:
        # Arto Inkala's "impossible" puzzle
        board = [
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ]
        # SudokuWiki Unsolvable #28 (takes a bit of time to beat)
        # board = [
        #     [6, 0, 0, 0, 0, 8, 9, 4, 0],
        #     [9, 0, 0, 0, 0, 6, 1, 0, 0],
        #     [0, 7, 0, 0, 4, 0, 0, 0, 0],
        #     [2, 0, 0, 6, 1, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0, 0, 2, 0, 0],
        #     [0, 8, 9, 0, 0, 2, 0, 0, 0],
        #     [0, 0, 0, 0, 6, 0, 0, 0, 5],
        #     [0, 0, 0, 0, 0, 0, 0, 3, 0],
        #     [8, 0, 0, 0, 0, 1, 6, 0, 0]
        # ]
    else:
        board = [[0] * 9 for i in range(9)]  # Setting up a empty sudoku board
        try:
            with urllib.request.urlopen("http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&?level=3") as url:
                data = json.loads(url.read().decode())
        except:
            with open('data.json') as json_file:
                json_objects = json.load(json_file)
                data = json_objects['sudoku_boards_data_base'][
                    random.randint(0, len(json_objects['sudoku_boards_data_base']))]

        if data['response']:
            for initial_sudoku_value in data['squares']:
                row_position = initial_sudoku_value['x']
                column_position = initial_sudoku_value['y']
                value_at_position = initial_sudoku_value['value']
                board[row_position][column_position] = value_at_position
    return board


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print(f'- - - - - - - - - - -')
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(f'| ', end="")
            if j == 8:
                print(board[i][j])
            else:
                print(f'{board[i][j]} ', end="")


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


def check_if_valid(board, input_number, position):
    # Check row
    for j in range(len(board[0])):
        if j != position[1] and board[position[0]][j] == input_number:
            return False
    # Check column
    for i in range(len(board)):
        if i != position[0] and board[i][position[1]] == input_number:
            return False
    # Check 3x3 box:
    box_starting_row = (position[0] // 3) * 3
    box_starting_column = (position[1] // 3) * 3
    for i in range(box_starting_row, box_starting_row + 3):
        for j in range(box_starting_column, box_starting_column + 3):
            if (i, j) != position and board[i][j] == input_number:
                return False
    return True  # Input number placement is valid


def solve(board):
    try_position = find_empty(board)
    if try_position is None:
        return True
    for number in range(1, 9 + 1):
        if check_if_valid(board, number, try_position):
            board[try_position[0]][try_position[1]] = number
            # Recursively try if picked numbers are correct solutions, if it's wrong, backtrack to try another number
            if solve(board):
                return True
            else:
                board[try_position[0]][try_position[1]] = 0
    # If all numbers from 1 to 9 are no longer valid, this solution patch in recursion is wrong and we need to backtrack
    return False


app = Flask(__name__)


@app.route("/sudoku")
def sudoku():
    board = generate_board()
    initial_board = [[value for value in row] for row in board]
    solve(board)
    solved_board = [[value for value in row] for row in board]
    return render_template("index.html", initial_board=initial_board, solved_board=solved_board)


if __name__ == "__main__":
    app.run()
