
# coding: utf-8

# Columbia-X--Assignment-03-Machine-Learning-Fundamentals

# # Set Up Session
import sys

class Sudoku(object):
    """ Sudoku state holder for backtracking search (BTS) based Sudoku solver

    Attributes:

    """
    # Board dimension:
    _N = 9

    # Empty assignment:
    _NULL = 0

    # Row names:
    _ROWS = 'ABCDEFGHI'
    # Col names:
    _COLS = '123456789'

    # Row constraints:
    _ROW_CONSTRAINTS = (
        ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'),
        ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'),
        ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'),
        ('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'),
        ('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'),
        ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'),
        ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'),
        ('H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'),
        ('I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9')
    )
    # Row constraints:
    _COL_CONSTRAINTS = (
        ('A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'),
        ('A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'),
        ('A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'),
        ('A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'),
        ('A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'),
        ('A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'),
        ('A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'),
        ('A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'),
        ('A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9')
    )
    # Grid constraints:
    _GRID_CONSTRAINTS = (
        # Top grids:
        ('A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'),
        ('A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'),
        ('A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'),
        # Center grids:
        ('D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'),
        ('D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'),
        ('D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'),
        # Bottom grids:
        ('G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'),
        ('G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'),
        ('G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9')
    )

    class Domain(object):
        """ Struct for domain state

        """
        def __init__(self):
            self.value = [True] * (Sudoku._N + 1)
            self.count = Sudoku._N

    def __init__(self, description):
        """ Initialize Sudoku state

        """
        # Assignment & domains:
        self._assignment = {}
        self._domain = {}
        self._constraint = {
            'row': {},
            'col': {},
            'grid': {}
        }
        self._feasible = {}

        # Assignment status:
        self._assigned = set()

        # Initialize assignment & domains:
        for row in Sudoku._ROWS:
            for col in Sudoku._COLS:
                cell = row + col
                self._assignment[cell] = Sudoku._NULL
                self._domain[cell] = Sudoku.Domain()

        # Initialize grid constraint
        for row_constraint in Sudoku._ROW_CONSTRAINTS:
            self._feasible[row_constraint] = [True] * (Sudoku._N + 1)
            for cell in row_constraint:
                self._constraint['row'][cell] = row_constraint

        # Initialize grid constraint
        for col_constraint in Sudoku._COL_CONSTRAINTS:
            self._feasible[col_constraint] = [True] * (Sudoku._N + 1)
            for cell in col_constraint:
                self._constraint['col'][cell] = col_constraint

        # Initialize grid constraint
        for grid_constraint in Sudoku._GRID_CONSTRAINTS:
            self._feasible[grid_constraint] = [True] * (Sudoku._N + 1)
            for cell in grid_constraint:
                self._constraint['grid'][cell] = grid_constraint

        # Set initial values:
        for index, val in enumerate(description):
            row, col = index // Sudoku._N, index % Sudoku._N
            cell = Sudoku._ROWS[row] + Sudoku._COLS[col]
            value = int(val)
            # Not empty assignment:
            if (Sudoku._NULL != value):
                self.set(cell, value)

    def is_assigned(self, cell):
        """ Whether the cell is assigned
        """
        return cell in self._assigned

    def _remove_from_domain(self, cell, value):
        """ Remove value from cell's domain

        """
        if (self._domain[cell].value)[value]:
            (self._domain[cell].value)[value] = False
            (self._domain[cell].count) -= 1

    def _propagate_constraint(self, cell, value):
        """ Propagate constraint

        """

        # Update constraints:
        self._feasible[self._constraint['row'][cell]][value] = False
        self._feasible[self._constraint['col'][cell]][value] = False
        self._feasible[self._constraint['grid'][cell]][value] = False

        # Update cell domains:
        cell_row, cell_col = cell

        for row in Sudoku._ROWS:
            row_cell = row + cell_col
            self._remove_from_domain(row_cell, value)
        for col in Sudoku._COLS:
            col_cell = cell_row + col
            self._remove_from_domain(col_cell, value)
        for grid_cell in self._constraint['grid'][cell]:
            self._remove_from_domain(grid_cell, value)

        # Finally:
        (self._domain[cell].value)[value] = False
        (self._domain[cell].count) -= 1

    def set(self, cell, value):
        """ Set cell value and propagate constraints

        """
        # Feasible assignment:
        if (self._domain[cell].value)[value]:
            # Set assignment:
            self._assignment[cell] = value
            self._assigned.add(cell)
            # Propagate constraint:
            self._propagate_constraint(cell, value)

    def is_consistent(self):
        """ Whether current assignment is consistent

        """
        return Sudoku._N ** 2 == len(self._assigned)

    def get_assignment(self):
        """ Return current assignment

        """
        # return "".join(str(self._assignment[row+col]) for row in Sudoku._ROWS for col in Sudoku._COLS) + " BTS"
        def get_row(row):
            return "".join(str(self._assignment[row+col]) for col in Sudoku._COLS)
        return "\n".join(get_row(row) for row in Sudoku._ROWS)

    def get_min_remaining_value_cell(self):
        """ Get next cell using minimum remaining values heuristics

        """
        # Initialize:
        min_remaining_values_count = Sudoku._N + 1
        min_remaining_values_cell = None

        # Update:
        for row in Sudoku._ROWS:
            for col in Sudoku._COLS:
                cell = row + col
                # Identify empty cell:
                if Sudoku._NULL == self._assignment[cell]:
                    # The unassigned cell has no feasible value:
                    if 0 == self._domain[cell].count:
                        return None
                    # Update MRV stats:
                    elif self._domain[cell].count < min_remaining_values_count:
                        min_remaining_values_count = self._domain[cell].count
                        min_remaining_values_cell = cell

        # Finally:
        return min_remaining_values_cell

    def get_ordered_cell_values(self, cell):
        """ Get feasible cell values using least constrained value heuristics

        """

        return [val for val in range(1, Sudoku._N + 1) if (self._domain[cell].value)[val]]

    def _add_to_domain(self, cell, value):
        """ Add value to cell's feasible domain

        """
        # After remove constraint, is the value feasible:
        feasible = (
            self._feasible[self._constraint['row'][cell]][value] and
            self._feasible[self._constraint['col'][cell]][value] and
            self._feasible[self._constraint['grid'][cell]][value]
        )

        if feasible and not (self._domain[cell].value)[value]:
            # Update:
            (self._domain[cell].value)[value] = True
            (self._domain[cell].count) += 1

    def _remove_constraint(self, cell, value):
        # Update constraints:
        self._feasible[self._constraint['row'][cell]][value] = True
        self._feasible[self._constraint['col'][cell]][value] = True
        self._feasible[self._constraint['grid'][cell]][value] = True

        # Update cell domains:
        cell_row, cell_col = cell

        for row in Sudoku._ROWS:
            row_cell = row + cell_col
            self._add_to_domain(row_cell, value)
        for col in Sudoku._COLS:
            col_cell = cell_row + col
            self._add_to_domain(col_cell, value)
        for grid_cell in self._constraint['grid'][cell]:
            self._add_to_domain(grid_cell, value)

        # Finally:
        (self._domain[cell].value)[value] = True
        (self._domain[cell].count) += 1

    def reset(self, cell, value):
        """ Reset cell value and remove previous set constraints

        """
        # Infeasible assignment:
        if not (self._domain[cell].value)[value]:
            # Reset assignment:
            self._assignment[cell] = Sudoku._NULL
            self._assigned.remove(cell)
            # Remove constaints:
            self._remove_constraint(cell, value)

# Main:
if __name__ == "__main__":
    # Precondition:
    if len(sys.argv) != 2:
        print("usage: python driver_3.py <input_string>")
        exit(1)

    # ## Parse Parameters
    # Sudoku description:
    SUDOKU_DESC = sys.argv[1]

    # Initialize:
    sudoku = Sudoku(SUDOKU_DESC)

    # BTS Sudoku solver:
    def bts(sudoku):
        if sudoku.is_consistent():
            return sudoku.get_assignment()

        cell = sudoku.get_min_remaining_value_cell()
        if not (cell is None):
            for value in sudoku.get_ordered_cell_values(cell):
                sudoku.set(cell, value)

                result = bts(sudoku)
                if not (result is None):
                    return result

                sudoku.reset(cell, value)
        return None

    # Solution:
    solved = bts(sudoku)

    """
    with open('output.txt') as descs:
        solved = "\n".join(bts(Sudoku(desc[:81])) for desc in descs)
    """

    with open("output.txt","w") as output:
        output.write(
            solved
        )
