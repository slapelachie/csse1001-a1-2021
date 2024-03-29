"""
Sliding Puzzle Game
Assignment 1
Semester 1, 2021
CSSE1001/CSSE7030
"""

from a1_support import *


__author__ = "Lachlan Slape, s4638520"
__email__ = "s4638520@student.uq.edu.au"


def shuffle_puzzle(solution: str) -> str:
    """
    Shuffle a puzzle solution to produce a solvable sliding puzzle.

    Parameters:
        solution (str): a solution to be converted into a shuffled puzzle.

    Returns:
        (str): a solvable shuffled game with an blank tile at the
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
    """
    Check if the user has one based on if the puzzle and the solution are the same

    Parameters:
        puzzle (str): the puzzle to be checked
        solution (str): the solved puzzle

    Returns:
        (str): Whether if the puzzle is solved or not

    """
    # Check if every character besides the last is the same
    return puzzle[:-1] == solution[:-1]


def swap_position(puzzle: str, from_index: int, to_index: int) -> str:
    """
    Swap the positions of two characters in a string

    Parameters:
        puzzle (str): the puzzle that has characters to be swapped
        from_index (int): The first chracter to be swapped
        to_index (int): The second character to be swapped

    Returns:
        (str): the puzzle with the characters swapped

    Note:
        An example of this function is given the puzzle as "abcd" and from_index
        as 0 and to_index as 2 would be from "abcd" -> "cbad"
    """
    puzzle_list = list(puzzle)

    # Used to swap the positons of the chracters in the array
    puzzle_list[from_index], puzzle_list[to_index] = (
        puzzle_list[to_index],
        puzzle_list[from_index],
    )
    return "".join(puzzle_list)


def move(puzzle: str, direction: str):
    """
    Move the blank tile to a position in the grid through the options up, down,
    left and right. Returns nothing if the tile cannot move to the specified
    location

    Parameters:
        puzzle (str): the puzzle where the blank tile will move
        direction (str): the direction for which the tile will move
                         only accepts "UP", "DOWN", "LEFT" and "RIGHT"

    Returns:
        (str): if the move was valid, the puzzle with the tile moved
        (None): if the move was not valid
    """
    position_index = puzzle.index(EMPTY)
    position = position_index + 1
    grid_width = get_grid_width(puzzle)

    # What direction to moved the tile if it's a valid move
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


def generate_grid(contents: str) -> str:
    """
    Generate the grid for the contents of a puzzle string based on the design
    +---+
    | a |
    +---+

    Parameters:
        contents (str): the contents of the puzzle to be generated in the grid

    Returns:
        (str): the grid the contains the characters within
    """
    grid = ""
    grid_width = get_grid_width(contents)

    # Generate each row of the grid
    for row in range(grid_width):
        # Add the seperator row
        grid += "{}\n".format(generate_grid_separator_row(grid_width))

        # Generate the row with characters in it
        for column in range(grid_width):
            position = (row * grid_width) + column
            grid += VERTICAL_WALL + EMPTY + contents[position] + EMPTY

        grid += "{}\n".format(VERTICAL_WALL)

    grid += generate_grid_separator_row(grid_width)

    return grid


def print_grid(puzzle: str) -> None:
    """
    Prints out the grid for the inputed puzzle string

    Parameters:
        puzzle (str): the puzzle string that is to be printed

    Returns:
        (None)
    """
    grid = generate_grid(puzzle)
    print(grid)


def generate_grid_separator_row(width: int) -> str:
    """
    Generate the seperator row for the grid based on the amount of characters
    to appear in that row
    Example: +---+---+---+

    Parameters:
        width (int): the amount of colums the row will have that contains
                     characters

    Returns:
        (str): the seperator row of the grid
    """
    row = ""

    for _ in range(width):
        row += CORNER + (3 * HORIZONTAL_WALL)

    row += CORNER
    return row


def get_grid_width(puzzle: str) -> int:
    """
    Get the width of the grid based on the size of the puzzle

    Parameters:
        puzzle (str): the puzzle

    Returns:
        (int) the width of the grid

    Note:
        The size of the puzzle must be a square otherwise the width will not
        reflect the proper size of the grid
    """
    return int(len(puzzle) ** (1 / 2))


def print_solution_position(solution: str, puzzle: str) -> None:
    """
    Print both the solution and the puzzle grid

    Parameters:
        solution (str): the solution of the puzzle string
        puzzle (str): the puzzle string

    Returns:
        (None)
    """
    print(
        "Solution:\n{}\n\nCurrent position:\n{}\n".format(
            generate_grid(solution), generate_grid(puzzle)
        )
    )


def main():
    """The main function that is executed when the file is run"""
    print(WELCOME_MESSAGE)

    playing = True
    while playing:

        # Valid inputs that the user can use
        move_actions = (UP, DOWN, LEFT, RIGHT)
        other_actions = (GIVE_UP, HELP)

        grid_size = int(input(BOARD_SIZE_PROMPT))

        # Get the puzzle and its solution
        solution = get_game_solution(WORDS_FILE, grid_size)
        puzzle = shuffle_puzzle(solution)

        solved = check_win(puzzle, solution)
        print_solution_position(solution, puzzle)

        # Continue to loop until the puzzle is solved or the user gives up
        while not solved:
            player_action = input(DIRECTION_PROMPT)

            # Player move input handler
            # Updates the puzzle with the new board layout, if fail alert user
            if player_action in move_actions:
                move_attempt = move(puzzle, player_action)
                if move_attempt:
                    puzzle = move_attempt
                else:
                    print(INVALID_MOVE_FORMAT.format(player_action))

            # Other inputs handler
            elif player_action in other_actions:
                if player_action == GIVE_UP:
                    break
                elif player_action == HELP:
                    print(HELP_MESSAGE)

            # If there is no match for input, alert the user
            else:
                print(INVALID_MESSAGE)

            print_solution_position(solution, puzzle)
            solved = check_win(puzzle, solution)

        # Show message depending if user won or not
        if solved:
            print(WIN_MESSAGE)
        else:
            print(GIVE_UP_MESSAGE)

        # Check if the user wishes to play again
        play_again = input(PLAY_AGAIN_PROMPT)
        if not (play_again.lower() == "y" or play_again == ""):
            playing = False
            print(BYE)


if __name__ == "__main__":
    main()
