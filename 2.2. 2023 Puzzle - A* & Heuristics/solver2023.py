#!/usr/local/bin/python3
# solver2023.py : 2023 Sliding tile puzzle solver
#
# Code by:
# Avishmita Mandal avmandal
# Aditya Padgal adpadgal
# Niharika Ganji nganji
#
# Based on skeleton code by B551 Staff, Fall 2023
#

import copy
import heapq
import sys

import numpy as np

ROWS = 5
COLS = 5


def printable_board(board):
    return [
        ("%3d ") * COLS % board[j : (j + COLS)] for j in range(0, ROWS * COLS, COLS)
    ]


def move_right(state, row):
    """Move the given row to one position right"""
    board = copy.deepcopy(state)
    board[row] = board[row][-1:] + board[row][:-1]
    return board


def move_left(state, row):
    board = copy.deepcopy(state)
    """Move the given row to one position left"""
    board[row] = board[row][1:] + board[row][:1]
    return board


def rotate_right(board, row, residual):
    board[row] = [board[row][0]] + [residual] + board[row][1:]
    residual = board[row].pop()
    return residual


def rotate_left(board, row, residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual = board[row].pop(0)
    return residual


def move_clockwise(state):
    """Move the outer ring clockwise"""
    board = copy.deepcopy(state)
    board[0] = [board[1][0]] + board[0]
    residual = board[0].pop()
    board = transpose_board(board)
    residual = rotate_right(board, -1, residual)
    board = transpose_board(board)
    residual = rotate_left(board, -1, residual)
    board = transpose_board(board)
    residual = rotate_left(board, 0, residual)
    board = transpose_board(board)
    return board


def move_cclockwise(state):
    """Move the outer ring counter-clockwise"""
    board = copy.deepcopy(state)
    board[0] = board[0] + [board[1][-1]]
    residual = board[0].pop(0)
    board = transpose_board(board)
    residual = rotate_right(board, 0, residual)
    board = transpose_board(board)
    residual = rotate_right(board, -1, residual)
    board = transpose_board(board)
    residual = rotate_left(board, -1, residual)
    board = transpose_board(board)
    return board


def transpose_board(board):
    """Transpose the board --> change row to column"""
    return [list(col) for col in zip(*board)]


def move_inner_ring_clockwise(board):
    state = np.array(board)
    inner_board = state[1:-1, 1:-1].tolist()
    inner_board = move_clockwise(inner_board)
    state[1:-1, 1:-1] = np.array(inner_board)
    return state.tolist()


def move_inner_ring_cc_clockwise(board):
    state = np.array(board)
    inner_board = state[1:-1, 1:-1].tolist()
    inner_board = move_cclockwise(inner_board)
    state[1:-1, 1:-1] = np.array(inner_board)
    return state.tolist()


# return a list of possible successor states
def successors(state):
    # List of successor states
    successors_state_list = []

    # 10 Successors whose rows are shifted horizontally
    for x in range(ROWS):
        # 1 cell right
        child_state = move_right(state, x)
        successors_state_list.append([child_state, "R" + str(x + 1)])

        # 1 cell left
        child_state = move_left(state, x)
        successors_state_list.append([child_state, "L" + str(x + 1)])

    # 10 Successors whose cols are shifted verically
    for x in range(COLS):
        # 1 cell up
        child_state = transpose_board(move_left(transpose_board(state), x))
        successors_state_list.append([child_state, "U" + str(x + 1)])

        # 1 cell down
        child_state = transpose_board(move_right(transpose_board(state), x))
        successors_state_list.append([child_state, "D" + str(x + 1)])

    # Outer ring - clockwise
    child_state = move_clockwise(state)
    successors_state_list.append([child_state, "Oc"])

    # Outer ring - counterclockwise
    child_state = move_cclockwise(state)
    successors_state_list.append([child_state, "Occ"])

    # Inner ring - clockwise
    child_state = move_inner_ring_clockwise(state)
    successors_state_list.append([child_state, "Ic"])

    # Inner ring - counterclockwise
    child_state = move_inner_ring_cc_clockwise(state)
    successors_state_list.append([child_state, "Icc"])

    return successors_state_list


# check if we've reached the goal
def is_goal(state):
    goal_state = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ]

    for i in range(5):
        for j in range(5):
            if goal_state[i][j] != state[i][j]:
                return False
    return True


# Manhattan distance
def calculate_heuristics(state):
    heuristic = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            target_i = (state[i][j] - 1) // 5
            target_j = (state[i][j] - 1) % 5
            heuristic += abs(i - target_i) + abs(j - target_j)

    return heuristic


# f(n) - g(n) + h(n), here f(n) is the evaluation function
def evaluation_function(state, cost):
    # Taking the adaptive cost used in path finding algorithms
    return calculate_heuristics(state) + 0.2 * pow(cost, 2)


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """

    initial_board = np.array(initial_board).reshape(ROWS, COLS).tolist()

    priority_queue = []
    eval_fn = evaluation_function(initial_board, 0)
    visited_states = set()

    combined_element = [eval_fn, initial_board, [], 0]
    heapq.heappush(priority_queue, combined_element)

    while priority_queue:
        (eval_fn, state, total_route, cost) = heapq.heappop(priority_queue)

        if is_goal(state):
            return total_route

        successors_state_list = successors(state)
        state_tuple = tuple(tuple(row) for row in state)

        if state_tuple not in visited_states:
            for element in successors_state_list:
                element_route = copy.deepcopy(total_route)
                successor_state = element[0]
                extended_route = element[1]
                element_route.append(extended_route)

                combined_element = [
                    evaluation_function(successor_state, cost + 1),
                    successor_state,
                    element_route,
                    cost + 1,
                ]
                heapq.heappush(priority_queue, combined_element)
            visited_states.add(state_tuple)

    return total_route


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], "r") as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != ROWS * COLS:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
