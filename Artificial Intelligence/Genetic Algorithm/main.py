import random

# Creating a population of random points
def gen_individuals(n): # n here stands for the degree of polynomial
    """
    Generate an individual with random coefficients for a polynomial of degree n.

    Parameters:
    n (int): The degree of the polynomial.

    Returns:
    list of float: A list of n random floating-point numbers.
    """
    return [random.uniform(-1000, 10000) for _ in range(n)]

# Fitting individual points to the polynomial for evaluating points
def fitness(co, individuals, r):
    """
    Evaluate the fitness of an individual solution based on how well it fits the polynomial equation.

    Parameters:
    co (list of float): The coefficients of the polynomial.
    individuals (list of float): The current set of values (individual) being evaluated.
    r (float): The constant term (right-hand side of the equation).

    Returns:
    float: The fitness score of the individual. A higher score indicates a better fit.
    """
    total = sum(co[i] * (individuals[i]** (i+1)) for i in range(len(co)))
    ans = total - r

    if ans == 0: # Hndle division by zero problem
        return 99999
    else:
        return abs(1/ans)

# Generating solutions
def gen_solotion(m): # m here stands for the degree of polynomial
    """
    Generate an initial population of potential solutions.

    Parameters:
    m (int): The degree of the polynomial.

    Returns:
    list of lists: A list containing 1000 individuals, each a list of m random floating-point numbers.
    """
    solutions = []
    for _ in range(1000):
        solutions.append(gen_individuals(m))
    return solutions

# Ranking each points by their function value
def rank_solutions(solutions, co, r):
    """
    Rank solutions based on their fitness scores.

    Parameters:
    solutions (list of lists): The current population of solutions.
    co (list of float): The coefficients of the polynomial.
    r (float): The constant term (right-hand side of the equation).

    Returns:
    list of lists: A list of solutions paired with their fitness scores, sorted in descending order by fitness.
    """
    ranked_solutions = []
    for s in solutions:
        ranked_solutions.append([fitness(co, s, r), s])
    ranked_solutions.sort(reverse=True)
    return ranked_solutions

# A function to mutate points.
def mutate(solutions, n, rate = 0.02):
    """
    Create a new generation of solutions by mutating the best solutions.

    Parameters:
    solutions (list of float): The best solutions from the previous generation.
    n (int): The degree of the polynomial.
    rate (float): The mutation rate, determining the degree of change applied.

    Returns:
    list of lists: A new generation of solutions created by mutating the input solutions.
    """
    # n here stands for the degree of polynomial
    newgeneration = []
    for _ in range(1000):
        selectedpoint = [random.choice(solutions) * random.uniform(1 - (rate/2), 1 + (rate/2)) for _ in range(n)] 
        newgeneration.append(selectedpoint)
    return newgeneration

# Main function of the algorithm
def genetic_algorithm(co, r):
    """
    Execute the genetic algorithm to find the best solution to fit the polynomial equation.

    Parameters:
    co (list of float): The coefficients of the polynomial.
    r (float): The constant term (right-hand side of the equation).

    Returns:
    None: The function prints the best solution for each generation until a solution is found or the maximum number of generations is reached.
    """
    n = len(co)
    solutions = gen_solotion(n)

    for i in range(1000):
        
        rankedsolutions = rank_solutions(solutions, co, r)

        # Display the best solution of the current generation
        print(f"Generation no.{i} best solution")
        print(f" Fitness value= {rankedsolutions[0][0]}")
        print(f"Coefficients={rankedsolutions[0][1]}")
        print("-------------------------------------------------------------")
        print("")

        if rankedsolutions[0][0] > 9999:
            break # Stop if a perfect solution is found

        # Select the top 100 solutions for mutation
        bestsolutions = rankedsolutions[:100]

        # Flatten the selected solutions for mutation
        elements = []
        for s in bestsolutions:
            for p in s[1]:
                elements.append(p)

        # Generate a new population by mutating the best solutions
        solutions = mutate(elements, n)

if __name__ == '__main__':
    # Example usage of the genetic algorithm
    co = [1, 2, 3] # Coefficients of the equation. If degree of your equation is n, then len(c) should be equal to n.
    r = 30 # Constant term of equation

    genetic_algorithm(co, r)
