"""62136"""


class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        """Return self == other."""
        return self.row == other.row and self.col == other.col

    def manhattan_distance(self, other):
        """
        Return the Manhattan distance between self and other.
        """
        return abs(self.row - other.row) + abs(self.col - other.col)


class State:
    def __init__(self, matrix):
        """
        Initilize a state with a matrix.
        @param matrix: list with N lists of N numbers, each unique;
        all numbers are from 0 to N^2-1
        """
        self.matrix = matrix
        self.matrix_size = len(matrix)

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
