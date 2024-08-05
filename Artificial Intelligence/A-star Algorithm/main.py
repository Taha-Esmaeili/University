import heapq


def heuristic(state, goal_col):
    """
    Calculate the heuristic for the A* search algorithm.

    The heuristic estimates the number of moves required for the red car (assumed to be the first car in the state list)
    to reach the goal column.

    Parameters:
    state (list of tuples): The current state of the parking lot, represented as a list of car tuples.
                            Each car tuple contains (row, column, orientation, length).
    goal_col (int): The column index that the red car needs to reach.

    Returns:
    int: The estimated number of moves required to reach the goal.
    """
    red_car = state[0]
    _, red_car_col, _, _ = red_car
    return goal_col - (red_car_col + 1)


def generate_moves(states, N, M):
    """
    Generate all possible valid moves for the current state of the parking lot.

    Parameters:
    states (list of tuples): The current state of the parking lot, represented as a list of car tuples.
                             Each car tuple contains (row, column, orientation, length).
    N (int): The number of rows in the parking lot.
    M (int): The number of columns in the parking lot.

    Returns:
    list of lists: A list of new states, each representing a valid move from the current state.
    """
    neighbors = []
    occupied = set()

    # Mark all occupied positions based on the current state of the cars
    for car in states:
        R, C, orientation, L = car
        if orientation == 'h':
            for i in range(L):
                occupied.add((R, C + i))
        else:
            for i in range(L):
                occupied.add((R + i, C))

    # Generate new states by moving each car in all possible directions
    for i, (R, C, orientation, L) in enumerate(states):
        if orientation == 'h': # Horizontal car
            # Move left
            for move in range(1, C):
                if all((R, C - j) not in occupied for j in range(1, move + 1)):
                    new_state = list(states)
                    new_state[i] = (R, C - move, orientation, L)
                    neighbors.append(new_state)
                else:
                    break
            # Move right
            for move in range(1, M - (C + L - 1) + 1):
                if all((R, C + L - 1 + j) not in occupied for j in range(1, move + 1)):
                    new_state = list(states)
                    new_state[i] = (R, C + move, orientation, L)
                    neighbors.append(new_state)
                else:
                    break
        else: # Vertical car
            # Move up
            for move in range(1, R):
                if all((R - j, C) not in occupied for j in range(1, move + 1)):
                    new_state = list(states)
                    new_state[i] = (R - move, C, orientation, L)
                    neighbors.append(new_state)
                else:
                    break
            # Move down
            for move in range(1, N - (R + L - 1) + 1):
                if all((R + L - 1 + j, C) not in occupied for j in range(1, move + 1)):
                    new_state = list(states)
                    new_state[i] = (R + move, C, orientation, L)
                    neighbors.append(new_state)
                else:
                    break

    return neighbors


def a_star(start_state, N, M):
    """
    Perform the A* search algorithm to solve the parking puzzle.

    Parameters:
    start_state (list of tuples): The initial state of the parking lot, represented as a list of car tuples.
                                  Each car tuple contains (row, column, orientation, length).
    N (int): The number of rows in the parking lot.
    M (int): The number of columns in the parking lot.

    Returns:
    int: The minimum number of moves required to solve the puzzle, or -1 if no solution exists.
    """
    goal_col = M
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start_state, goal_col), 0, start_state))
    came_from = {}
    g_score = {tuple(start_state): 0}
    f_score = {tuple(start_state): heuristic(start_state, goal_col)}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        # Check if the red car (first car) has reached the goal column
        if current[0][1] + 1 == goal_col:
            return current_g

        for neighbor in generate_moves(current, N, M):
            tentative_g_score = current_g + 1
            neighbor_tuple = tuple(tuple(car) for car in neighbor)

            if tentative_g_score < g_score.get(neighbor_tuple, float('inf')):
                came_from[neighbor_tuple] = current
                g_score[neighbor_tuple] = tentative_g_score
                f_score[neighbor_tuple] = tentative_g_score + heuristic(neighbor, goal_col)
                if neighbor_tuple not in [i[2] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor_tuple], tentative_g_score, neighbor))

    return -1


def main(parkings):
    """
    Solve a series of parking puzzles using the A* search algorithm.

    Parameters:
    parkings (list of tuples): A list of parking puzzles, where each puzzle is represented by a tuple (N, M, cars).
                               N is the number of rows, M is the number of columns, and cars is a list of car tuples.

    Returns:
    list of str: A list of results for each puzzle, indicating the test number and the minimum number of moves required.
    """
    results = []

    for i in range(len(parkings)):
        N, M, cars = parkings[i]
        result = a_star(cars, N, M)
        results.append(f"Test #{i + 1}: {result}")

    return results




if __name__ == "__main__":
    """
    Main execution block for solving multiple parking puzzles.

    The program reads input from the user, where the first line contains the number of test cases (T).
    For each test case, the grid dimensions (N, M) and the number of vehicles (V) are provided, followed
    by the details of each vehicle (R, C, orientation, L).

    The program then solves each puzzle using the A* algorithm and prints the results.
    """
    
    T = int(input()) # Number of test cases

    parkings = []

    for _ in range(T):
        N, M, V = map(int, input().split()) # Grid dimensions and number of vehicles
        cars = []
        for _ in range(V):
            R, C, orientation, L = input().split()
            R, C, L = int(R), int(C), int(L)
            cars.append((R, C, orientation, L))
        parkings.append((N, M, cars))

    results = main(parkings)
    for result in results:
        print(result)
