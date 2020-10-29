"""62136"""

from copy import deepcopy


class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Coordinate({self.row}, {self.col})"

    def __eq__(self, other):
        """Return self == other."""
        return self.row == other.row and self.col == other.col

    def __add__(self, other):
        """Return self + other."""
        return Coordinate(self.row + other.row, self.col + other.col)

    def is_valid(self, limit):
        """
        Return `True` if the coordinate is valid for a matrix of size `limit`.
        """
        return 0 <= self.row < limit and 0 <= self.col < limit

    def manhattan_distance(self, other):
        """
        Return the Manhattan distance between self and other.
        """
        return abs(self.row - other.row) + abs(self.col - other.col)


class Action:
    def __init__(self, name, zero_delta):
        """
        Initialize an action with a name and the difference in the
        coordinates of the 0 element.
        """
        self.name = name
        self.delta = zero_delta

    def __repr__(self):
        return f"Action({self.name}, {self.delta})"


class Actions:
    ALL = [
        Action("left", Coordinate(0, +1)),
        Action("right", Coordinate(0, -1)),
        Action("up", Coordinate(+1, 0)),
        Action("down", Coordinate(-1, 0)),
    ]


class State:
    def __init__(self, matrix):
        """
        Initilize a state with a matrix.
        @param matrix: list with N lists of N numbers, each unique;
        all numbers are from 0 to N^2-1
        """
        self.matrix = matrix
        self.matrix_size = len(matrix)

    def __repr__(self):
        return f"State({self.matrix})"

    @property
    def coordinates(self):
        """
        Return a dictionary with the coordinates in the matrix of each number.
        """
        return {
            self.matrix[i][j]: Coordinate(i, j)
            for j in range(self.matrix_size)
            for i in range(self.matrix_size)
        }

    def heuristic(self, goal_state):
        """
        Return Manhattan distance heuristics for a given goal state.
        """
        goal_state_coordinates = goal_state.coordinates
        return sum(
            coordinate.manhattan_distance(goal_state_coordinates[number])
            for (number, coordinate) in self.coordinates.items()
            if number != 0
        )

    def successors(self):
        """
        Return all tuples with successor states and
        the action needed to create the state.
        """
        zer_coord = self.coordinates[0]
        legal_moves = [
            action for action in Actions.ALL
            if (zer_coord + action.delta).is_valid(self.matrix_size)
        ]
        states = []
        for move in legal_moves:
            new_zero = zer_coord + move.delta
            number_to_move = self.matrix[new_zero.row][new_zero.col]
            new_matrix = deepcopy(self.matrix)
            new_matrix[zer_coord.row][zer_coord.col] = number_to_move
            new_matrix[new_zero.row][new_zero.col] = 0
            states.append(State(new_matrix))

        return list(zip(states, legal_moves))
