"""62136"""


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Return self == other."""
        return self.x == other.x and self.y == other.y

    def manhattan_distance(self, other):
        """
        Return the Manhattan distance between self and other.
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


class State:
    def __init__(self, matrix, matrix_size):
        """
        Initilize a state with a matrix.
        @param matrix: list with N lists of N numbers, each unique; all numbers are from 0 to N^2-1
        @param matrix_size: N - the size of one side of the matrix
        """
        self.matrix = matrix
        self.matrix_size = matrix_size


    @property
    def coordinates(self):
        return {
            self.matrix[i][j]: Coordinate(j, i)
            for j in range(self.matrix_size)
            for i in range(self.matrix_size)
            if self.matrix[i][j] != 0
        }


    def heuristic(self, goal_state):
        """
        Return Manhattan distance heuristics for a given goal state.
        """
        goal_state_coordinates = goal_state.coordinates # let's not compute it each iteration
        return sum(
            coordinate.manhattan_distance(goal_state_coordinates[number])
            for (number, coordinate) in self.coordinates.items()
        )
