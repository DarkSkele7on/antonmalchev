import sys

# Define the list of possible operators and the number of numbers required
OPS = ['+', '-', '*', '/']
NUMS_REQUIRED = 4


def find_optimal_expression(numbers):
    """Given a list of numbers, return a string that represents the expression
    that uses one set of brackets and evaluates to 10 if possible. If no such
    expression exists, return None.
    """

    # Iterate over all possible operator combinations
    for op1 in OPS:
        for op2 in OPS:
            for op3 in OPS:

                # Form the two possible expressions with brackets
                expr1 = f'({numbers[0]} {op1} {numbers[1]}) {op2} ({numbers[2]} {op3} {numbers[3]})'
                expr2 = f'{numbers[0]} {op1} ({numbers[1]} {op2} ({numbers[2]} {op3} {numbers[3]}))'

                # Evaluate the expressions and check if either of them equals 10
                result1 = eval(expr1)
                result2 = eval(expr2)
                if abs(result1 - 10) < 0.0001:
                    return expr1
                elif abs(result2 - 10) < 0.0001:
                    return expr2

    # If no expression evaluates to 10, return None
    return None


# Continuously read input numbers from the console
while True:
    try:
        # Read input numbers and check for end condition
        inputs = input(f"Enter {NUMS_REQUIRED} space-separated numbers, or 'end' to exit: ")
        if inputs == 'end':
            sys.exit()
        numbers = [float(n) for n in inputs.split()]
        if len(numbers) != NUMS_REQUIRED:
            print(f"Please enter exactly {NUMS_REQUIRED} numbers.")
            continue

        # Find the optimal expression and print the result
        expr = find_optimal_expression(numbers)
        if expr:
            print(f"Optimal expression: {expr}")
        else:
            print("No expression evaluates to 10.")
    except ValueError:
        print("Please enter valid numbers.")
