import json
import random
import urllib.request
from urllib.error import URLError


def generate_board():
    """
    Generates initial sudoku board
    """
    board = [[0] * 9 for _ in range(9)]  # Setting up a empty sudoku board
    try:
        with urllib.request.urlopen(url="http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&?level=3?qwe") as url:
            data = json.loads(url.read().decode())
    except URLError as e:
        with open(file='data.json') as json_file:
            json_objects = json.load(json_file)
            data = json_objects['sudoku_boards_data_base'][
                random.randint(0, len(json_objects['sudoku_boards_data_base']))]
        print("Error code: ", e.reason)

    if data['response']:
        for initial_sudoku_value in data['squares']:
            row_position = initial_sudoku_value['x']
            column_position = initial_sudoku_value['y']
            value_at_position = initial_sudoku_value['value']
            board[row_position][column_position] = value_at_position

    return board


def is_row_valid(board, row):
    """
    Checks if all values in a row are valid (no duplicates)
    """
    set_for_check = set()
    for j in range(0, 9):
        if board[row][j] in set_for_check:
            return False
        elif board[row][j] != 0:
            set_for_check.add(board[row][j])
    return True


def is_col_valid(board, col):
    """
    Checks if all values in a collumn are valid (no duplicates)
    :param board: Sudoku board
    :param col: Selected column in sudoku board
    """
    set_for_check = set()
    for i in range(0, 9):
        if board[i][col] in set_for_check:
            return False
        elif board[i][col] != 0:
            set_for_check.add(board[i][col])
    return True


def is_box_valid(board, start_row, start_col):
    """
    Checks if all values in a box (3x3 in sudoku board grid) are valid (no duplicates)
    :param board: Sudoku board
    :param start_row: Selected starting row for a 3x3 box in sudoku board
    :param start_col: Selected starting column for a 3x3 box in sudoku board
    """
    set_for_check = set()
    for row in range(3):
        for col in range(3):
            value = board[row + start_row][col + start_col]
            if value in set_for_check:
                return False
            if value != 0:
                set_for_check.add(value)
    return True


def three_checks_for_validation(board, row, col):
    """
    Checks for three options: row, column and 3x3 box to validate sudoku board
    :param board: Sudoku board
    :param col: Selected row in sudoku board
    :param col: Selected column in sudoku board
    """
    return is_row_valid(board, row) and is_col_valid(board, col) and is_box_valid(board, row - row % 3, col - col % 3)


def check_if_board_is_valid(board):
    """
    Checks if provided board is valid
    :param board: Sudoku board
    """
    for i in range(9):
        for j in range(9):
            if not three_checks_for_validation(board, i, j):
                return False
    return True


def print_board(board):
    """
    Prints current sudoku board state
    :param board: Sudoku board
    """
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - -')
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print('| ', end="")
            if j == 8:
                print(board[i][j])
            else:
                print('{board[i][j]} ', end="")


def find_empty(board):
    """
    Finds an empty cell in current sudoku board state
    :param board: Sudoku board
    :return: Coordinates x, y of of an empty cell in current sudoku board state, None if not found
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


def check_if_input_is_valid(board, input_number, position):
    """
    Checks if the input_number at position in currend sudoku board state is valid
    :param board: Sudoku board
    :param input_number: Value to input in a cell
    :param position: List of [x, y] coordinates of a cell to try to input the input_number to
    :return: True if input_number at position is valid, False if it's not
    """
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


def place_at_position(board, input_number, position):
    """
    Inputs the input_number at position in currend sudoku board state
    :param board: Sudoku board
    :param input_number: Value to input in a cell
    :param position: Tuple of [x, y] coordinates of a cell to input the input_number to
    """
    board[position[0]][position[1]] = input_number


def solve(board):
    """
    Recursively try to brute force a solution to initial sudoku board
    :param board: Sudoku board
    :return: True if solution found, False if it's not found
    """
    try_position = find_empty(board=board)
    if try_position is None:
        return True
    for number in range(1, 9 + 1):
        if check_if_input_is_valid(board=board, input_number=number, position=try_position):
            place_at_position(board=board, input_number=number, position=try_position)
            # Recursively try if picked numbers are correct solutions, if it's wrong, backtrack to try another number
            if solve(board=board):
                return True
            place_at_position(board=board, input_number=0, position=try_position)
    # If all numbers from 1 to 9 are no longer valid, this solution patch in recursion is wrong and we need to backtrack
    return False


if __name__ == "__main__":
    current_board = generate_board()
    initial_board = [[value for value in row] for row in current_board]
    print("Initial board:")
    for row in initial_board:
        print(row)
    print()
    solve(board=current_board)
    solved_board = [[value for value in row] for row in current_board]
    if solved_board != initial_board:
        print("Solved board:")
        for row in solved_board:
            print(row)
    else:
        print("Initial board is not solvable")
