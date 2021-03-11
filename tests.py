import unittest
import a1
import random


class AssignmentTest(unittest.TestCase):
    def test_shuffle_puzzle(self):
        puzzle = a1.shuffle_puzzle("abcd")
        self.assertEqual(puzzle[-1:], " ")

    def test_swap_position(self):
        puzzle = a1.swap_position("care", 0, 2)
        self.assertEqual(puzzle, "race")

        puzzle = a1.swap_position("does", 2, 3)
        self.assertEqual(puzzle, "dose")

    def test_check_win(self):
        win = a1.check_win("abcd ", "abcde")
        self.assertTrue(win)

        win = a1.check_win("abcde ", "abcdef")
        self.assertTrue(win)

        win = a1.check_win("abcdef ", "abcdefg")
        self.assertTrue(win)

        win = a1.check_win("bd ac", "abcde")
        self.assertFalse(win)

    def test_get_grid_width(self):
        width = a1.get_grid_width("abcd")
        self.assertEqual(width, 2)

        width = a1.get_grid_width("abcdefghi")
        self.assertEqual(width, 3)

    def test_generate_grid_separator_row(self):
        row_length = random.randint(0, 9)
        row_len = (row_length * 4) + 1
        row = a1.generate_grid_separator_row(row_length)
        self.assertEqual(row_len, len(row))

    def test_generate_grid(self):
        grid = a1.generate_grid("abcd")
        self.assertEqual(
            grid,
            """+---+---+
| a | b |
+---+---+
| c | d |
+---+---+""",
        )

    def test_move_three(self):
        puzzle = "abcd efgh"

        puzzle_moved = a1.move(puzzle, "U")
        self.assertEqual(puzzle_moved, "a cdbefgh")

        puzzle_moved = a1.move(puzzle, "D")
        self.assertEqual(puzzle_moved, "abcdgef h")

        puzzle_moved = a1.move(puzzle, "L")
        self.assertEqual(puzzle_moved, "abc defgh")

        puzzle_moved = a1.move(puzzle, "R")
        self.assertEqual(puzzle_moved, "abcde fgh")

    def test_move_two(self):
        puzzle = "ab c"

        puzzle_moved = a1.move(puzzle, "U")
        self.assertEqual(puzzle_moved, " bac")

        puzzle_moved = a1.move(puzzle, "R")
        self.assertEqual(puzzle_moved, "abc ")
