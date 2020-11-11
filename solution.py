"""62136"""

from copy import deepcopy
from math import sqrt
from queue import PriorityQueue


class Coordinate:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        """Return repr(self)."""
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
        """Return repr(self)."""
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
        """Return repr(self)."""
        return f"State({self.matrix})"

    def __eq__(self, other):
        """Return self == other."""
        return self.matrix == other.matrix

    def __hash__(self):
        """Return hash(self)."""
        return hash(tuple(tuple(row) for row in self.matrix))

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
        Return [(State, Action)] - a list of tuples with all successor states
        with the corresponding moves to them.
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


class Node:
    """Represents a node in the state tree."""

    def __init__(self, state, goal_state, parent=None, action_name=None):
        self.state = state
        self.heuristic = self.state.heuristic(goal_state)
        self.depth = 0 if parent is None else parent.depth + 1
        self.parent = parent
        self.action_name = action_name

    def f(self):
        """
        Return the evaluation f(self) where
        f(self) = g(self) + h(self)
        g(self) ::= the cost to get to the state i.e. its depth
        h(self) ::= calculated heuristics of the state
        """
        return self.depth + self.heuristic

    def __lt__(self, other):
        """Return self < other."""
        return self.f() < other.f()


class Solution:
    """Utility class to help with the solution of the specific problem."""

    def __init__(self):
        self.init_state = None
        self.goal_state = None
        self.output = None

    def parse(self, input_str):
        input_lines = input_str.split('\n')
        num_tiles = int(input_lines[0])
        matrix_size = int(sqrt(num_tiles + 1))
        zero_pos = int(input_lines[1])

        # Goal state

        tiles = list(range(1, num_tiles + 1))
        if zero_pos == -1:
            tiles.append(0)
        else:
            tiles.insert(zero_pos, 0)

        goal_matrix = [
            [tiles[i + j] for j in range(matrix_size)]
            for i in range(0, len(tiles), matrix_size)
        ]

        self.goal_state = State(goal_matrix)

        # Initial state

        init_matrix = [
            list(map(int, line.split()))
            for line in input_lines[2:-1]
        ]

        self.init_state = State(init_matrix)

    def solve(self):
        """
        Solve the problem using A* algorithm and store the solution
        in `self.output`.
        """
        path = self.__astar(self.init_state, self.goal_state)
        self.output = str(len(path)) + "\n" + "\n".join(path) + "\n"

    def __astar(self, root, goal):
        """
        Return the optimal path from `root` to `goal`
        using the A* algorithm.
        """
        if root == goal:
            return []

        queue = PriorityQueue()
        expanded = {root}
        root_node = Node(root, goal)

        # first level
        moves = root.successors()
        for move in moves:
            if move[0] == goal:
                return [move[1].name]
            node = Node(move[0], goal, root_node, move[1].name)
            queue.put(node)
            expanded.add(move[0])

        # next levels
        current = root_node
        while True:
            current = queue.get()

            if current.state == goal:
                break

            moves = current.state.successors()
            for move in moves:
                if move[0] in expanded:
                    continue

                node = Node(move[0], goal, current, move[1].name)
                queue.put(node)
                expanded.add(move[0])

        # path
        result = []
        while current.parent is not None:
            result.append(current.action_name)
            current = current.parent

        return result[::-1]


if __name__ == "__main__":
    from sys import stdin, stdout
    solution = Solution()
    solution.parse(stdin.read())
    solution.solve()
    stdout.write(solution.output)
