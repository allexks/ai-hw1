"""Unit tests."""

import unittest
from solution import Coordinate, State, Solution


class Tests(unittest.TestCase):
    def test_manhattan_distance_correct(self):
        """Test that manhattan distance computes correctly."""
        c1 = Coordinate(0, 0)
        c2 = Coordinate(2, 3)
        expect = 5

        result1 = c1.manhattan_distance(c2)
        result2 = c2.manhattan_distance(c1)

        self.assertEqual(expect, result1)
        self.assertEqual(expect, result2)

    def test_coordinates_equal(self):
        """Test that two same coordinates are equal."""
        c1 = Coordinate(1, 1)
        c2 = Coordinate(1, 1)
        d = c1.manhattan_distance(c2)

        self.assertEqual(c1, c2)
        self.assertEqual(0, d)

    def test_coordinates_valid(self):
        """Test the validity of coordinates."""
        limit = 3
        c1 = Coordinate(2, 2)
        c2 = Coordinate(-1, 1)
        c3 = Coordinate(0, 3)

        v1 = c1.is_valid(limit)
        v2 = c2.is_valid(limit)
        v3 = c3.is_valid(limit)

        self.assertTrue(v1)
        self.assertFalse(v2)
        self.assertFalse(v3)

    def test_coordinates_addition(self):
        """Test that 2 coordinates add up correctly."""
        c1 = Coordinate(1, 2)
        c2 = Coordinate(-1, 1)
        expect = Coordinate(0, 3)

        result = c1 + c2

        self.assertEqual(expect, result)

    def test_state_coordinates_correct(self):
        """Test that `State.coordinates` produces correct coordinates."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]
        s = State(matrix)
        expect = {
            1: Coordinate(0, 0),
            2: Coordinate(0, 1),
            3: Coordinate(0, 2),
            4: Coordinate(1, 0),
            5: Coordinate(1, 1),
            6: Coordinate(1, 2),
            7: Coordinate(2, 0),
            8: Coordinate(2, 1),
            0: Coordinate(2, 2),
        }

        result = s.coordinates

        self.assertEqual(expect, result)

    def test_state_eq(self):
        """Test that two equal states are equal."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]

        s1 = State(matrix)
        s2 = State(matrix)

        self.assertEqual(s1, s2)

    def test_state_hash(self):
        """Test that the state hash is deterined by its matrix."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]
        s = State(matrix)
        expect_tuple = (
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 0),
        )
        expect = hash(expect_tuple)

        result = hash(s)

        self.assertEqual(expect, result)

    def test_heuristics_of_goal_is_zero(self):
        """Test that the heuristic function of the goal state is 0."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]
        state = State(matrix)
        goal = State(matrix)

        result = state.heuristic(goal)

        self.assertEqual(0, result)

    def test_heuristics_correct(self):
        """Test that the heuristic function is generally correct."""
        state_matrix = [
            [2, 1, 3],
            [4, 0, 5],
            [6, 7, 8],
        ]
        goal_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]
        s = State(state_matrix)
        g = State(goal_matrix)
        expect = 8

        result = s.heuristic(g)

        self.assertEqual(expect, result)

    def test_successors_two(self):
        """Test generating two successors."""
        state_matrix = [
            [0, 2, 3],
            [1, 4, 5],
            [6, 7, 8],
        ]
        s = State(state_matrix)
        expect_matrixes = [
            [
                [2, 0, 3],
                [1, 4, 5],
                [6, 7, 8],
            ],
            [
                [1, 2, 3],
                [0, 4, 5],
                [6, 7, 8],
            ],
        ]
        expect_moves = ["left", "up"]

        result = s.successors()

        self.assertEqual(2, len(result))
        self.assertEqual(expect_matrixes, [s[0].matrix for s in result])
        self.assertEqual(expect_moves, [s[1].name for s in result])

    def test_successors_three(self):
        """Test generating three successors."""
        state_matrix = [
            [1, 2, 3],
            [0, 4, 5],
            [6, 7, 8],
        ]
        s = State(state_matrix)
        expect_matrixes = [
            [
                [1, 2, 3],
                [4, 0, 5],
                [6, 7, 8],
            ],
            [
                [1, 2, 3],
                [6, 4, 5],
                [0, 7, 8],
            ],
            [
                [0, 2, 3],
                [1, 4, 5],
                [6, 7, 8],
            ],
        ]
        expect_moves = ["left", "up", "down"]

        result = s.successors()

        self.assertEqual(3, len(result))
        self.assertEqual(expect_matrixes, [s[0].matrix for s in result])
        self.assertEqual(expect_moves, [s[1].name for s in result])

    def test_successors_four(self):
        """Test generating four successors."""
        state_matrix = [
            [1, 2, 3],
            [4, 0, 5],
            [6, 7, 8],
        ]
        s = State(state_matrix)
        expect_matrixes = [
            [
                [1, 2, 3],
                [4, 5, 0],
                [6, 7, 8],
            ],
            [
                [1, 2, 3],
                [0, 4, 5],
                [6, 7, 8],
            ],
            [
                [1, 2, 3],
                [4, 7, 5],
                [6, 0, 8],
            ],
            [
                [1, 0, 3],
                [4, 2, 5],
                [6, 7, 8],
            ],
        ]
        expect_moves = ["left", "right", "up", "down"]

        result = s.successors()

        self.assertEqual(4, len(result))
        self.assertEqual(expect_matrixes, [s[0].matrix for s in result])
        self.assertEqual(expect_moves, [s[1].name for s in result])

    def test_parse_goal_state_minus_one(self):
        """Test that the zero is last in the goal state when -1 is read."""
        inp = "8\n"\
            "-1\n"\
            "1 2 3\n"\
            "4 5 6\n"\
            "0 7 8\n"
        s = Solution()
        expect = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],
        ]

        s.parse(inp)

        self.assertEqual(expect, s.goal_state.matrix)

    def test_parse_goal_state_normal(self):
        """Test that the zero is in the correct index in the goal state."""
        inp = "8\n"\
            "5\n"\
            "1 2 3\n"\
            "4 5 6\n"\
            "0 7 8\n"
        s = Solution()
        expect = [
            [1, 2, 3],
            [4, 5, 0],
            [6, 7, 8],
        ]

        s.parse(inp)

        self.assertEqual(expect, s.goal_state.matrix)

    def test_parse_init_state_size_three(self):
        """Test that the init state reading with size 3."""
        inp = "8\n"\
            "-1\n"\
            "1 2 3\n"\
            "4 5 6\n"\
            "0 7 8\n"
        s = Solution()
        expect = [
            [1, 2, 3],
            [4, 5, 6],
            [0, 7, 8],
        ]

        s.parse(inp)

        self.assertEqual(expect, s.init_state.matrix)

    def test_parse_init_state_size_four(self):
        """Test that the init state reading with size 4."""
        inp = "15\n"\
            "-1\n"\
            "1 2 3 9\n"\
            "4 5 6 10\n"\
            "0 7 8 11\n"\
            "12 13 14 15\n"
        s = Solution()
        expect = [
            [1, 2, 3, 9],
            [4, 5, 6, 10],
            [0, 7, 8, 11],
            [12, 13, 14, 15],
        ]

        s.parse(inp)

        self.assertEqual(expect, s.init_state.matrix)

    def test_parse_init_state_size_five(self):
        """Test that the init state reading with size 5."""
        inp = "24\n"\
            "-1\n"\
            "1 2 3 9 16\n"\
            "4 5 6 10 17\n"\
            "0 7 8 11 18\n"\
            "12 13 14 15 19\n"\
            "20 21 22 23 24\n"
        s = Solution()
        expect = [
            [1, 2, 3, 9, 16],
            [4, 5, 6, 10, 17],
            [0, 7, 8, 11, 18],
            [12, 13, 14, 15, 19],
            [20, 21, 22, 23, 24],
        ]

        s.parse(inp)

        self.assertEqual(expect, s.init_state.matrix)

    def test_3x3_depth_2(self):
        """Test with the given basic example."""
        self.__load_test_case_from_file("8-2")

    def test_3x3_depth_8(self):
        """Test with a 3x3 board and 8-step solution."""
        self.__load_test_case_from_file("8-8")

    def test_3x3_depth_21(self):
        """Test with a 3x3 board and a 21-step solution."""
        self.__load_test_case_from_file("8-21")

    def test_3x3_depth_31(self):
        """Test with a 3x3 board and a 31-step solution."""
        self.__load_test_case_from_file("8-31")

    def __load_test_case_from_file(self, name):
        folder = "test_cases"

        with open(f"{folder}/{name}.in", "r") as fin:
            inp = fin.read()

        with open(f"{folder}/{name}.out", "r") as fout:
            expect = fout.read()

        s = Solution()
        s.parse(inp)
        s.solve()
        result = s.output

        self.assertEqual(expect, result)


if __name__ == "__main__":
    unittest.main()
