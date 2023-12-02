import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(10, 10, num_rows, num_cols, 5, 5)
        self.assertEqual(
                len(m1._cells),
                num_rows,
        )
        self.assertEqual(
                len(m1._cells[0]),
                num_cols,
        )

        m1._break_entrance_and_exit()
        self.assertEqual(
                m1._cells[0][0].has_left_wall or m1._cells[0][0].has_right_wall,
                False,
        )
        exit_cell = m1._cells[num_rows - 1][num_cols -1]
        self.assertEqual(
                exit_cell.has_left_wall or exit_cell.has_right_wall,
                False,
        )

        m1._reset_cells_visited()
        visited = False
        for i in range(num_rows-1):
            for j in range(num_cols-1):
                if m1._cells[i][j].visited:
                    visited = True
        self.assertEqual(
                visited,
                False,
        )

if __name__ == "__main__":
    unittest.main()

