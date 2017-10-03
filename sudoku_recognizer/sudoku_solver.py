#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Sudoku Solver


    MIT License

    Copyright (c) 2017 Simon Berger

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import itertools


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
squares = cross(rows, cols)
unitlist = (
    [cross(rows, c) for c in cols] +
    [cross(r, cols) for r in rows] +
    [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
)

units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)


def parse_grid(grid):
    """
        Convert grid to a dict of possible values, {square: digits}, or
        return False if a contradiction is detected.
    """

    grid = "".join(str(v) for v in itertools.chain(*grid))
    # To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # (Fail if we can't assign d to square s.)
    return values


def convert_to_grid(parsed_grid):
    if not parsed_grid:
        return False

    grid = [[0 for _ in range(9)] for _ in range(9)]

    for key, value in parsed_grid.items():
        row_key, column_key = key

        row = rows.index(row_key)
        column = digits.index(column_key)

        grid[row][column] = value

    return grid


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."

    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    """
        Eliminate all the other values (except d) from values[s] and propagate.
        Return values, except return False if a contradiction is detected.
    """

    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """
        Eliminate d from values[s]; propagate when values or places <= 2.
        Return values, except return False if a contradiction is detected.
    """

    if d not in values[s]:
        return values  # Already eliminated
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


def solve(grid):
    """
        Solve the 2-dimensional list representing a Sudoku grid where 0 represents an empty field
    """

    return convert_to_grid(search(parse_grid(grid)))


def search(values):
    "Using depth-first search and propagation, try all possible values."

    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) for d in values[s])


def some(seq):
    "Return some element of seq which evaluates to true"

    for e in seq:
        if e:
            return e

    return False


def render_grid(grid):
    """
        A little extra function mainly used for debugging which nicely renders a grid into a string like so:

        5 3 4  6 7 8  9 1 2
        6 7 2  1 9 5  3 4 8
        1 9 8  3 4 2  5 6 7

        8 5 9  7 6 1  4 2 3
        4 2 6  8 5 3  7 9 1
        7 1 3  9 2 4  8 5 6

        9 6 1  5 3 7  2 8 4
        2 8 7  4 1 9  6 3 5
        3 4 5  2 8 6  1 7 9
    """

    if not grid:  # just in case
        return "No solution"

    lines = []

    for col in grid:
        packs = [" ".join(str(val) for val in col[i:i + 3]) for i in range(0, len(col), 3)]  # create packs of three numbers each >> ["5 3 4", "6 7 8", "9 1 2"]
        line = "  ".join(packs)  # combine them with extra space >> "5 3 4  6 7 8  9 1 2"
        lines.append(line)  # add this to the list of lines

    packs = ["\n".join(lines[i:i + 3]) for i in range(0, len(lines), 3)]  # create packs of three lines and seperate them with a simple line break
    final = "\n\n".join(packs)  # combine these packs with an extra line break

    return final

if __name__ == "__main__":
    def test():
        """
            Test the Solver
        """
        import time  # used to display the time it took to display it

        # sample Sudoku taken from Wikipedia https://en.wikipedia.org/wiki/File:Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

        print("Solving\n---\n{}\n---\n".format(render_grid(grid)))
        start_time = time.time()

        solved = solve(grid)

        # print(solved)
        print("SOLVED\n---\n{}\n---\nit took {} milliseconds".format(render_grid(solved), round(1000 * (time.time() - start_time))))

    test()
