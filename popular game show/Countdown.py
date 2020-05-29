"""
@author: Vaibhavi Dharashivkar
"""
# imports
import random
import sys

# global variable
overall_best = sys.maxsize


def swap(a, b, state, target):
    """
    In this function we take 2 numbers as input which are the index values in our states and then we interchange the
    values at those particular index places.
    :param a: Number 1
    :param b: Number 2
    :param state: initial expression for this iteration
    :param target: Evaluating the expression should give a value as close as the target
    :return: new state expression and target-result
    """
    # a = random.randrange(0, 200, 2)
    # b = random.randrange(0, 200, 2)
    new_state = ''
    for i in range(len(state)):
        if i == a:
            new_state += state[b]
            continue
        if i == b:
            new_state += state[a]
            continue
        new_state += state[i]
    # print(new_state)
    res = solving(int(new_state[0]), int(new_state[2]), new_state[1])
    for i in range(2, len(new_state) - 2, 2):
        res = solving(res, int(new_state[i + 2]), new_state[i + 1])
    # print("Distance from target: ", target - res)
    return new_state, abs(target - res)


def change(a, b, state, target):
    """
    In this function we take 2 input one is the index value and the other is the operator value. Chance the operator
    at index specified by 'a' with the value specified in 'b'.
    :param a: Number 1
    :param b: Number 2
    :param state: initial expression for this iteration
    :param target: Evaluating the expression should give a value as close as the target
    :return: new state expression and target-result
    """
    # a = random.randrange(1, 199, 2)
    # b = random.randrange(1, 199, 2)
    new_state = ''
    for i in range(len(state)):
        if i == a:
            new_state += b
            continue
        new_state += state[i]
    # print(new_state)
    res = solving(int(new_state[0]), int(new_state[2]), new_state[1])
    for i in range(2, len(new_state) - 2, 2):
        res = solving(res, int(new_state[i + 2]), new_state[i + 1])
    # print("Distance from target: ", target - res)
    return new_state, abs(target - res)


def next_state_generation(state, target, operators):
    """
    In the function, the closed to the target value and state is returned from amongst all the states that can be
    reached by either swapping 2 numbers from the previous state or by changing an operator at a particular position
    in the previous state
    :param state: initial state (expression) of the iteration
    :param target: Evaluating the expression should give a value as close as the target
    :param operators: A list of all the possible operators that can be used which are: '*','/','+','-'
    :return: returns the best value generated from all the neighbour states of the previous state
    """
    current_swap_state = ''
    current_swap_res = sys.maxsize
    current_change_state = ''
    current_change_res = sys.maxsize
    # for swapping
    for i in range(0, len(state), 2):
        for j in range(2, len(state), 2):
            new_swap_state, swap_res = swap(i, j, state, target)
            if current_swap_res > swap_res:
                current_swap_res = swap_res
                current_swap_state = new_swap_state
    # for changing
    for i in range(1, len(state) - 1, 2):
        new_change_state, change_res = change(i, random.choice(operators), state, target)
        if current_change_res > change_res:
            current_change_res = change_res
            current_change_state = new_change_state
    # return the lowest of the 2 value and state amongst swapping and changing operations
    print("Swap res:", current_swap_res)
    print("Change res:", current_change_res)
    if current_swap_res < current_change_res:
        print("Best State ", current_swap_state)
        print("Distance from target: ", current_swap_res)
        print()
        return current_swap_state, current_swap_res
    else:
        print("Best State ", current_change_state)
        print("Distance from target: ", current_change_res)
        print()
        return current_change_state, current_change_res


def initial_state(numbers, operators, target):
    """
    In this function the initial state and its distance from the target is calculated and returned for each iteration
    :param numbers: The original list of random numbers the user has
    :param operators: A list of all the possible operators that can be used which are: '*','/','+','-'
    :param target: Evaluating the expression should give a value as close as the target
    :return: Returns the initial state and result for every iteration
    """
    x = numbers
    opt = random.choice(operators)
    random.shuffle(x)
    state = str(x[0]) + opt + str(x[1])
    res = solving(x[0], x[1], opt)
    for i in range(2, len(x)):
        op = random.choice(operators)
        state += op + str(x[i])
        res = solving(res, x[i], op)
    print("S0:", state)
    print("Distance from target: ", abs(target - res))
    print()
    return state, abs(target - res)


def solving(num1, num2, opt):
    """
    This function is used as a supplement to solve for the result of evaluating an expression with 2 variables and an
    operator
    :param num1: Number 1
    :param num2: Number 2
    :param opt: operators that can be given as an input which are: '*','/','+','-'
    :return: result of evaluation of the expression
    """
    res = 0
    if opt == '*':
        res = num1 * num2
    elif opt == '/':
        try:
            res = num1 / num2
        except ZeroDivisionError:
            res = 0
    elif opt == '+':
        res = num1 + num2
    elif opt == '-':
        res = num1 - num2
    return abs(res)


def iterations(numbers, operators, target):
    """
    This function is used to calculate the best state and the best value for each iteration and pass the value of the
    current best to compare it with the overall best
    :param numbers: The original list of random numbers the user has
    :param operators: A list of all the possible operators that can be used which are: '*','/','+','-'
    :param target: Evaluating the expression should give a value as close as the target
    :return: The best value is returned after every iteration
    """
    state, res = initial_state(numbers, operators, target)
    current_state = state
    current_res = res

    next_state, next_res = next_state_generation(current_state, target, operators)
    while next_res < current_res:
        current_res = next_res
        current_state = next_state
    return current_res


if __name__ == '__main__':
    numbers = []
    i = 1
    operators = ['*', '/', '+', '-']
    target = random.randint(1000, 9999)
    # target = 3127
    for x in range(100):
        numbers.append(random.randint(0, 9))
    print(numbers)
    print("Target is: ", target)
    while True:
        print("***************************************************************")
        print("RR Iteration: ", i)
        result = iterations(numbers, operators, target)
        if result < overall_best:
            overall_best = result
        print("overall_best", overall_best)
        i += 1


# Numbers: [3, 3, 7, 3, 3, 4, 6, 7, 3, 5, 8, 2, 7, 6, 4, 4, 1, 2, 2, 8, 3, 2, 3, 0, 2, 3, 3, 7, 7, 3, 2, 9, 0, 2, 0, 4,
# 3, 0, 2, 7, 1, 3, 7, 1, 7, 0, 7, 8, 4, 1, 9, 9, 2, 3, 5, 0, 4, 9, 1, 4, 6, 0, 1, 1, 4, 5, 1, 9, 7, 4, 5, 3, 7, 2, 9,
# 7, 2, 0, 1, 8, 1, 4, 3, 9, 3, 5, 3, 6, 6, 8, 9, 7, 7, 9, 4, 6, 7, 1, 6, 6]
# Target: 3127

# run1
# Best state: 9+0+4/2-4*7*3-7-7*1/8+7+9/0*2+0+1*4+4*7+8/5*5*3-3-3-5-7-7/9+8+9/7+8/1+4*4-9-4+6-3-3*4+0+1+2/2-3*8+1-2+0
# /0*3+3*1+1*3/6-9+2/7/2+4*6-1-1-9/9*0-9-6*3/7-7*5-2*4*6+4+5/7-6-0*2+2/3+6/3+1-3+2+3*7+3*6-1*3+7-7
# value: 0.857142857143117
# run time: 60 seconds

# run 2
# Best State: 1/8*6-2/3*7-7*7-3/1+6-9/4*1+5*7+5+8*1/9/3+2-9*4*4+7+6*3+7+7*9+2/4+2*7-1*2*0+1*3/5-1/0*2/9/1-3+1+7-0*7+0+
# 2+3*2/4+8+3*9+0+7+5/8*8/3*5+6*4-3-0/7*0/3/2-7/6/6+2+7+3-3+7/1+2-0*3*3+9/4*9+4-3*6-9+4+6+1+4/3*4
# Value: 1.5
# run time: 30 seconds

# run 3
# Best State: 3+6*2/9-5+8*4/7+1/6+5/3*7/3-1-4-4-1-2/1*0-7+1/2*8/7*1/0/0+3-6-3+3/9/3/7+2-7*6-2-7+7/7*9/3+5*2-7+4+7/4/1/
# 3-3+4/0/4+9*8+0/7+7*3+4*2-4-5*6/2-6/2/5/7-3/0*3+3/7/2+9-3-0-0+1*8+4-1*9-6-1/4-9-8*3+1-3-9+6+2*9
# value: 28.14285714285643
# run time: 10 seconds
