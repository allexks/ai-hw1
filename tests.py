"""Unit tests."""

import unittest
from solution import Coordinate, State


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

    def test_manhattan_distance_equals(self):
        """Test that two same coordinates are equal."""
        c1 = Coordinate(1, 1)
        c2 = Coordinate(1, 1)
        d = c1.manhattan_distance(c2)

        self.assertEqual(c1, c2)
        self.assertEqual(0, d)

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


if __name__ == "__main__":
    unittest.main()
