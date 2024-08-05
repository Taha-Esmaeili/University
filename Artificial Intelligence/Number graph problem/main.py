def get_leftmost_digit(number):
    """
    Get the leftmost digit of a number.

    Parameters:
    number (int): The number from which to extract the leftmost digit.

    Returns:
    int: The leftmost digit of the number.
    """
    return int(str(number)[0])


def get_rightmost_digit(number):
    """
    Get the rightmost digit of a number.

    Parameters:
    number (int): The number from which to extract the rightmost digit.

    Returns:
    int: The rightmost digit of the number.
    """
    return int(str(number)[-1])


def calculate_product(values):
    """
    Calculate the product of a list of values.

    Parameters:
    values (list of int): The list of values to multiply.

    Returns:
    int: The product of the values.
    """
    result = 1
    for value in values:
        result *= value
    return result


def calculate_sum(values):
    """
    Calculate the sum of a list of values.

    Parameters:
    values (list of int): The list of values to sum.

    Returns:
    int: The sum of the values.
    """
    return sum(values)


def is_assignment_valid(assignment, shapes, edges):
    """
    Check if a given assignment of values to nodes is valid based on the shapes and connections.

    The validity is determined by specific rules depending on the shape of the node:
    - 'T': The node's value should match the leftmost digit of the product of its neighbors' values.
    - 'S': The node's value should match the rightmost digit of the product of its neighbors' values.
    - 'P': The node's value should match the leftmost digit of the sum of its neighbors' values.
    - 'H': The node's value should match the rightmost digit of the sum of its neighbors' values.

    Parameters:
    assignment (dict): The current assignment of values to nodes.
    shapes (list of str): The shape associated with each node.
    edges (dict): The adjacency list representing the graph's edges.

    Returns:
    bool: True if the assignment is valid, False otherwise.
    """
    for node, shape in enumerate(shapes):
        neighbors = [assignment[neighbor] for neighbor in edges[node]]
        if shape == 'T' and assignment[node] != get_leftmost_digit(calculate_product(neighbors)):
            return False
        if shape == 'S' and assignment[node] != get_rightmost_digit(calculate_product(neighbors)):
            return False
        if shape == 'P' and assignment[node] != get_leftmost_digit(calculate_sum(neighbors)):
            return False
        if shape == 'H' and assignment[node] != get_rightmost_digit(calculate_sum(neighbors)):
            return False
    return True


def backtrack_assignment(assignment, shapes, edges, domain):
    """
    Perform a backtracking search to find a valid assignment of values to nodes.

    The function recursively assigns values to nodes and checks if the assignment is valid.
    If an assignment is found that satisfies all the constraints, it is returned.
    Otherwise, the function backtracks and tries a different assignment.

    Parameters:
    assignment (dict): The current partial assignment of values to nodes.
    shapes (list of str): The shape associated with each node.
    edges (dict): The adjacency list representing the graph's edges.
    domain (range): The range of possible values that can be assigned to nodes.

    Returns:
    dict or None: A valid assignment if one is found, None otherwise.
    """
    if len(assignment) == len(shapes):
        if is_assignment_valid(assignment, shapes, edges):
            return assignment
        else:
            return None

    current_variable = len(assignment)
    for value in domain:
        if value not in assignment.values():  
            assignment[current_variable] = value
            result = backtrack_assignment(assignment, shapes, edges, domain)
            if result is not None:
                return result
            del assignment[current_variable]

    return None


def solve_CSP(num_nodes, num_edges, shapes, edges):
    """
    Solve the constraint satisfaction problem (CSP) for the given graph.

    The CSP involves assigning values to nodes such that the constraints based on the shapes of the nodes are satisfied.

    Parameters:
    num_nodes (int): The number of nodes in the graph.
    num_edges (int): The number of edges in the graph.
    shapes (list of str): The shape associated with each node.
    edges (dict): The adjacency list representing the graph's edges.

    Returns:
    str: A string representing the solution if found, or a message indicating that no solution was found.
    """
    domain_values = range(1, 10)
    solution = backtrack_assignment({}, shapes, edges, domain_values)

    if solution is None:
        return "No solution found"

    return ' '.join(str(solution[node]) for node in range(num_nodes))



if __name__ == "__main__":
    """
    Main execution block for solving multiple test cases of the CSP.

    The program reads input from the user, where the first line contains the number of test cases.
    For each test case, the number of nodes, edges, and the shape of each node are provided,
    followed by the edges between nodes. The program then solves the CSP for each test case
    and prints the result.
    """
    num_test_cases = int(input())

    for _ in range(num_test_cases):
        num_nodes, num_edges = map(int, input().split())
        shapes = input().split()
        edge_dict = {i: [] for i in range(num_nodes)}

        for _ in range(num_edges):
            node1, node2 = map(int, input().split())
            edge_dict[node1].append(node2)
            edge_dict[node2].append(node1)

        result = solve_CSP(num_nodes, num_edges, shapes, edge_dict)
        print(result)
