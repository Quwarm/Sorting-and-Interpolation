#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Example of using Lagrange interpolation.

Program with a menu for working with numerical data.
Allows you to perform the following operations with data (points):
1. Adding data from the console.
2. Displaying data in the console.
3. Delete data.
4. Data sorting.
5. Interpolation of a segment.
6. The definition of the function on the points.

Libraries:
1. Matplotlib: https://pypi.org/project/matplotlib/
2. Decimal (standart). https://pypi.org/project/cdecimal/
3. Lagrange interpolation. https://github.com/Quwarm/Sorting-and-Interpolation
"""
from matplotlib import pyplot
from decimal import Decimal, getcontext
from lagrange_interpolation import point_interpolation, interpolation_formula

#############################################
#############################################
#############################################
# Variables and arrays to work with
X, Y = list(), list()
N_SIZE = len(X)
NUM_TYPE = Decimal
# ACCURACY - the higher the value, the more accurate the interpolation result
# (750 for 50 elements up to 6 decimal places)
ACCURACY = 200
getcontext().prec = ACCURACY
# MAIN_STEP - a variable that defines the current stage of the program work
# 0 - initial, 1 - data sorted and ready for interpolation
MAIN_STEP = 0


#############################################
#############################################
#############################################
# Defining functions for working with data

# Entering a number with type checking, inf and 0
def input_parameter(param_type):
    """
    A function that allows the user to enter a parameter with the type specified in the argument param_type.
    :param param_type: The type of number that the user must enter.
    """
    while True:
        param_str = input()
        try:
            param = param_type(param_str)
        except:
            print('#> Invalid input. Repeat again: ', end='')
            continue
        if isinstance(param, (float, Decimal)) and (param == Decimal('inf') or -param == Decimal('inf')):
            print('#> The number is too exponential. Repeat again: ', end='')
            continue
        if param == NUM_TYPE(0) and param_str != '0' and param_str != '0.0':
            print('#> The number is too small exponentially. Repeat again: ', end='')
            continue
        return param


# Adding points
def add_points():
    """
    A function that allows the user to add a point from the console.
    """
    global X, Y, N_SIZE
    print('Add points')
    while True:
        print('#> Enter X and Y: ', end='')
        str_list = input().split()
        try:
            x, y = NUM_TYPE(str_list[0]), NUM_TYPE(str_list[1])
        except:
            return  # Exit if input is incorrect
        if x in X:
            print('This X coordinate is already in the list')
            continue
        if isinstance(x, (float, Decimal)) and (x == Decimal('inf') or -x == Decimal('inf')):
            print('X coordinate too exponential')
            continue
        if isinstance(y, (float, Decimal)) and (y == Decimal('inf') or -y == Decimal('inf')):
            print('Y coordinate too exponential')
            continue
        if x == NUM_TYPE(0) and str_list[0] != '0' and str_list[0] != '0.0':
            print('X coordinate is too small exponentially')
            continue
        if y == NUM_TYPE(0) and str_list[1] != '0' and str_list[1] != '0.0':
            print('Y coordinate is too small exponentially')
            continue
        X.append(x)
        Y.append(y)
        N_SIZE = len(X)


# Data cleaning
def del_points():
    """
    A function that deletes all data (points).
    """
    global X, Y, N_SIZE
    N_SIZE = 0
    X.clear()
    Y.clear()


# Displaying points on the console in regular or exponential form
def show_points():
    """
    A function that displays point data in the console.
    """
    global X, Y, N_SIZE
    print('Enter display type', '1: regular format (0.001)', '2: exponential format (1E-3): ', ':> ', sep='\n', end='')
    format_number = input_parameter(int)
    while format_number != 1 and format_number != 2:
        print('#> Invalid input. Repeat again: ', end='')
        format_number = input_parameter(int)
    format_number = '\n{:+F} {:+F}' if format_number == 1 else '\n{:+E} {:+E}'
    print(*[format_number.format(X[i], Y[i]) for i in range(N_SIZE)], end='\n\n')


# Shell Sort
def shell_sort():
    """
    A function that performs a sort of Shell.
    """
    global X, Y, N_SIZE
    step = N_SIZE // 2
    while step > 0:
        i = step
        while i < N_SIZE:
            j = 0
            while j < i:
                if X[j] > X[i]:
                    X[j], X[i] = X[i], X[j]
                    Y[j], Y[i] = Y[i], Y[j]
                j += 1
            i += 1
        step = step // 2


# Segment interpolation
def segment_interpolation_lagrange():
    """
    A function that performs interpolation of a segment based on global arrays X and H and parameters entered by the user.
    """
    global X, Y, N_SIZE
    # Entering interpolation parameters
    print('#> Degree of interpolation (1-' + str(N_SIZE) + '): ', end='')
    nPoints = input_parameter(int)
    while nPoints < 1 or nPoints > N_SIZE:
        print('#> Invalid input. Repeat again: ', end='')
        nPoints = input_parameter(int)

    print('#> Starting coordinate: ', end='')
    fStart = input_parameter(NUM_TYPE)

    print('#> Final coordinate: ', end='')
    fStop = input_parameter(NUM_TYPE)
    while fStart >= fStop:
        print('!> The final coordinate should be greater than the starting one.', '#> Repeat again: ', sep='\n', end='')
        fStop = input_parameter(NUM_TYPE)

    print('#> Number of break points (1-10000000): ', end='')
    nSplit = input_parameter(int)
    while nSplit < 1 or nSplit > 10000000:
        print('#> Invalid input. Repeat again: ', end='')
        nSplit = input_parameter(int)

    print('#> Linear (1) or point (2) graph: ', end='')
    nGraphType = input_parameter(int)
    while nGraphType != 1 and nGraphType != 2:
        print('#> Invalid input. Repeat again: ', end='')
        nGraphType = input_parameter(int)

    # Determining the difference between two adjacent points
    nSplitSize = (fStop - fStart) / (nSplit - 1)
    iPos = 0  # The position from which the X coordinate search begins
    nX, nY = list(), list()  # Temporary arrays
    TempX = fStart  # Start from the starting coordinate
    while TempX <= fStop:
        # Go through the list X until we find a suitable coordinate
        # (greater than or equal to TempX)
        while iPos < N_SIZE and X[iPos] < TempX:
            iPos += 1
        nxStart = iPos - nPoints  # Start index
        nxStop = iPos + nPoints  # Stop index
        # If going beyond, then reset to default values
        nxStart = 0 if (nxStart < 0) else nxStart
        nxStop = N_SIZE if (nxStop > N_SIZE) else nxStop
        # Point interpolation
        result = point_interpolation(X, Y, nxStart, nxStop, TempX)
        # Adding results to the temporary lists
        nX.append(TempX)
        nY.append(result)
        # Increment the counter by the size of the split
        TempX += nSplitSize
    # Graph
    if nGraphType == 1:
        pyplot.plot(nX, nY, linewidth=2)
    else:
        pyplot.scatter(nX, nY, 2)
    pyplot.title('Graph')
    pyplot.grid(True)
    pyplot.show()
    # Delete temporary arrays
    del nX
    del nY


# Setting a new precision
def set_accuracy():
    """
    A function that determines the accuracy of represented real numbers.
    """
    global ACCURACY
    print('Enter the accuracy of the values (10 <= accuracy <= 10000, recommended to use \'750\'): ', end='')
    ACCURACY = input_parameter(int)
    while ACCURACY < 10 or ACCURACY >= 10000:
        print('#> Invalid input. Repeat again: ', end='')
        ACCURACY = input_parameter(int)
    getcontext().prec = ACCURACY


# Defining a function by points
def print_polynomial():
    """
    A function that outputs the Lagrange polynomial for global arrays X and Y at a user-specified precision.
    """
    global X, Y, ACCURACY
    print('Enter the precision of the values (0 <= precision < accuracy, recommended to use \'6\'): ', end='')
    precision = input_parameter(int)
    while precision < 0 or precision > ACCURACY:
        print('#> Invalid input. Repeat again: ', end='')
        precision = input_parameter(int)
    print('Enter display type', '1: regular format (0.001)', '2: exponential format (1E-3)', ':> ', sep='\n', end='')
    format_number = input_parameter(int)
    while format_number != 1 and format_number != 2:
        print('#> Invalid input. Repeat again: ', end='')
        format_number = input_parameter(int)
    format_number = '{:+.' + str(precision) + 'F}*x^{}' if format_number == 1 else '{:+.' + str(precision) + 'E}*x^{}'
    print('f(x) =', interpolation_formula(X, Y, precision, format_number))


#############################################
#############################################
#############################################
# Menu
def menu(is_loop=True):
    """
    Function that determines the operation to be performed on the data based on user input.
    :param is_loop: whether the function should run indefinitely in a loop until '0' is entered.
    """
    global N_SIZE, MAIN_STEP
    while is_loop:
        print('--------Menu---------')
        print('Accuracy: ' + str(ACCURACY))
        print(str(N_SIZE) + ' points')
        print('1. Add points from the console')
        if N_SIZE > 0:
            print('2. View all points')
        if N_SIZE > 1:
            print('3. Delete all points')
            print('4. Sort')
        if MAIN_STEP == 1:
            print('5. Interpolate a segment')
            print('6. Define a function by points')
        print('---------------------')
        print('*. Set accuracy')
        print('0. Exit')
        print('#> ', end='')
        item = input()
        if item == '0':
            exit(0)
        elif item == '1':
            add_points()
            MAIN_STEP = 0
        elif N_SIZE > 0 and item == '2':
            show_points()
        elif N_SIZE > 1 and item == '3':
            del_points()
            MAIN_STEP = 0
        elif N_SIZE > 1 and item == '4':
            shell_sort()
            MAIN_STEP = 1
        elif N_SIZE > 1 and MAIN_STEP == 1 and item == '5':
            segment_interpolation_lagrange()
        elif N_SIZE > 1 and MAIN_STEP == 1 and item == '6':
            print_polynomial()
        elif item == '*':
            set_accuracy()
        else:
            print('Invalid input')
        N_SIZE = len(X)
        print('---------------------')


if __name__ == '__main__':
    menu()
