"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""

import math

from a1_support import *


__author__ = "Lachlan Slape, 46385200"
__email__ = "s4638520@student.uq.edu.au"


def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.

    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.

    Returns:
        (str): a solvable shuffled game with an empty tile at the
               bottom right corner.

    References:
        - https://en.wikipedia.org/wiki/15_puzzle#Solvability
        - https://www.youtube.com/watch?v=YI1WqYKHi78&ab_channel=Numberphile

    Note: This function uses the swap_position function that you have to
          implement on your own. Use this function when the swap_position
          function is ready
    """
    shuffled_solution = solution[:-1]

    # Do more shuffling for bigger puzzles.
    swaps = len(solution) * 2
    for _ in range(swaps):
        # Pick two indices in the puzzle randomly.
        index1, index2 = random.sample(range(len(shuffled_solution)), k=2)
        shuffled_solution = swap_position(shuffled_solution, index1, index2)

    return shuffled_solution + EMPTY


def check_win(puzzle: str, solution: str) -> bool:
    # TODO: Make this human readable
    return puzzle[: (len(solution) - 1)] == solution[: (len(solution) - 1)]


def swap_position(puzzle: str, from_index: int, to_index: int) -> str:
    puzzle_list = list(puzzle)
    puzzle_list[from_index], puzzle_list[to_index] = (
        puzzle_list[to_index],
        puzzle_list[from_index],
    )
    return "".join(puzzle_list)


def move(puzzle: str, direction: str):
    position_index = get_position(puzzle)
    position = position_index + 1
    grid_width = get_grid_width(puzzle)

    if direction == UP:
        if (position) > grid_width:
            return swap_position(puzzle, position_index, position_index - grid_width)

    elif direction == DOWN:
        if (len(puzzle) - position) >= grid_width:
            return swap_position(puzzle, position_index, position_index + grid_width)

    elif direction == LEFT:
        if (position - 1) % grid_width != 0:
            return swap_position(puzzle, position_index, position_index - 1)

    elif direction == RIGHT:
        if position % grid_width != 0:
            return swap_position(puzzle, position_index, position_index + 1)

    return None


def get_position(puzzle: str) -> int:
    return puzzle.index(EMPTY)


def print_grid(puzzle: str) -> None:
    grid = generate_grid(puzzle)
    print(grid)
    return None


def generate_grid(contents: str) -> str:
    grid = ""
    grid_width = get_grid_width(contents)

    for row in range(grid_width):
        grid += generate_grid_row(grid_width) + "\n"
        for column in range(grid_width):
            position = (row * grid_width) + column
            grid += VERTICAL_WALL + EMPTY + contents[position] + EMPTY
        grid += "{}\n".format(VERTICAL_WALL)

    grid += generate_grid_row(grid_width)

    return grid


def generate_grid_row(width: int) -> str:
    row = ""
    for _ in range(width):
        row += CORNER + (3 * HORIZONTAL_WALL)

    row += CORNER
    return row


def get_grid_width(puzzle: str) -> int:
    return int(math.sqrt(len(puzzle)))


def print_solution_position(solution: str, puzzle: str) -> None:
    print("Solution:")
    print(generate_grid(solution))
    print("")
    print("Current position:")
    print(generate_grid(puzzle))
    print("")


def game_loop():
    move_inputs = (UP, DOWN, LEFT, RIGHT)
    other_inputs = (GIVE_UP, HELP)

    grid_size = int(input(BOARD_SIZE_PROMPT))

    solution = get_game_solution(WORDS_FILE, grid_size)
    puzzle = shuffle_puzzle(solution)
    solved = check_win(puzzle, solution)

    print_solution_position(solution, puzzle)

    while not solved:

        player_input = input(DIRECTION_PROMPT)

        if player_input in move_inputs:
            move_attempt = move(puzzle, player_input)
            if move_attempt:
                puzzle = move_attempt
                print_solution_position(solution, puzzle)
            else:
                print(INVALID_MOVE_FORMAT.format(player_input))

        elif player_input in other_inputs:
            if player_input == GIVE_UP:
                break
            elif player_input == HELP:
                print(HELP_MESSAGE)

        else:
            print(INVALID_MESSAGE)

        solved = check_win(puzzle, solution)

    if solved:
        print(WIN_MESSAGE)
    else:
        print(GIVE_UP_MESSAGE)

    play_again = input(PLAY_AGAIN_PROMPT)
    if play_again.lower() == "y" or play_again == "":
        game_loop()
    else:
        print(BYE)


def main():
    print(WELCOME_MESSAGE)
    game_loop()


if __name__ == "__main__":
    main()
