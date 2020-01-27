import matplotlib.pyplot as pyplot

X, Y = list(), list()
nSize = len(X)

# A variable that defines the current stage of the program work
# 0 - initial, 1 - data sorted and ready for interpolation
main_step = 0


#############################################
#############################################
#############################################
# Logical part 1. Basic operations with input data

# Add points
def add_points():
    global X, Y, nSize
    print('Add points')
    while True:
        print('#> Enter X and Y: ')
        str_list = input().split()
        try:
            x, y = float(str_list[0]), float(str_list[1])
        except Exception:
            # Exit if input is incorrect
            return
        if x in X:
            print('This X coordinate is already in the list.')
            continue
        if (x == float('inf')) or (-x == float('inf')):
            print('X coordinate too exponential')
            continue
        if (y == float('inf')) or (-y == float('inf')):
            print('Y coordinate too exponential')
            continue
        if x == 0 and str_list[0] != '0' and str_list[0] != '0.0':
            print('X coordinate is too small exponentially')
            continue
        if y == 0 and str_list[1] != '0' and str_list[1] != '0.0':
            print('Y coordinate is too small exponentially')
            continue
        X.append(x)
        Y.append(y)
        nSize = len(X)


# Clear lists X and Y
def cls_points():
    global X, Y, nSize
    nSize = 0
    X.clear()
    Y.clear()


# Display points in the console in an exponential form
def show_points():
    global X, Y, nSize
    print('Enter display type', '1: regular format (0.001)', '2: exponential format (1E-3): ', ':> ',
          sep='\n', end='')
    format_number = input_parameter('int')
    while format_number < 1 or format_number > 2:
        print('#> Invalid input. Repeat again: ')
        format_number = input_parameter('int')
    format_number = '\n' + ('{:+F} {:+F}' if format_number == 1 else '{:+E} {:+E}')
    print(*[format_number.format(X[i], Y[i]) for i in range(nSize)], end='\n\n')


# Shell Sort
def shell_sort():
    global X, Y, main_step, nSize
    step = nSize // 2
    while step > 0:
        i = step
        while i < nSize:
            j = 0
            while j < i:
                if X[j] > X[i]:
                    X[j], X[i] = X[i], X[j]
                    Y[j], Y[i] = Y[i], Y[j]
                j += 1
            i += 1
        step = step // 2
    main_step = 1


# Interpolation of a single point by the Lagrange method
def point_interpolation(nStart, nStop, x):
    global X, Y
    ntResult = 0.0
    i = nStart
    while i < nStop:
        ntProduct = Y[i]
        j = nStart
        while j < nStop:
            if i != j:
                ntProduct *= (x - X[j]) / (X[i] - X[j])
            j += 1
        ntResult += ntProduct
        i += 1
    return ntResult


# Entering a number with type checking, inf and 0
def input_parameter(param_type):
    param = None
    while True:
        param_str = input()
        try:
            if param_type == 'int':
                param = int(param_str)
            elif param_type == 'float':
                param = float(param_str)
        except Exception:
            print('#> Invalid input. Repeat again: ')
            continue
        if param == float('inf') or -param == float('inf'):
            print('#> The number is too exponential. Repeat again: ')
            continue
        if param == 0 and param_str != '0' and param_str != '0.0':
            print('#> The number is too small exponentially. Repeat again: ')
            continue
        return param


# Segment interpolation
def interpolation():
    global X, Y, nSize
    # Entering interpolation parameters
    print('#> Degree of interpolation (1-' + str(nSize) + '): ')
    nPoints = input_parameter('int')
    while nPoints < 1 or nPoints > nSize:
        print('#> Invalid input. Repeat again: ')
        nPoints = input_parameter('int')

    print('#> Starting coordinate: ')
    fStart = input_parameter('float')

    print('#> Final coordinate: ')
    fStop = input_parameter('float')
    while fStart >= fStop:
        print('!> The final coordinate should be greater than the starting one.\n#> Repeat again: ')
        fStop = input_parameter('float')

    print('#> Number of break points (1-10000000): ')
    nSplit = input_parameter('int')
    while nSplit < 1 or nSplit > 10000000:
        print('#> Invalid input. Repeat again: ')
        nSplit = input_parameter('int')

    print('#> Linear (1) or point (2) graph: ')
    nGraphType = input_parameter('int')
    while nGraphType != 1 and nGraphType != 2:
        print('#> Invalid input. Repeat again: ')
        nGraphType = input_parameter('int')

    # Determining the difference between two adjacent points
    nSplitSize = (fStop - fStart) / (nSplit - 1)
    iPos = 0  # The position from which the X coordinate search begins
    nX, nY = list(), list()  # Temporary arrays
    TempX = fStart  # Start from the starting coordinate
    while TempX <= fStop:
        # Go through the list X until we find a suitable coordinate
        # (greater than or equal to TempX)
        while iPos < nSize and X[iPos] < TempX:
            iPos += 1
        nxStart = iPos - nPoints  # Start index
        nxStop = iPos + nPoints  # Stop index
        # If going beyond, then reset to default values
        nxStart = 0 if (nxStart < 0) else nxStart
        nxStop = nSize if (nxStop > nSize) else nxStop
        # Point interpolation
        result = point_interpolation(nxStart, nxStop, TempX)
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


#############################################
#############################################
#############################################
# Logical part 2. Definition of the interpolation formula

# Polynomial addition function
def polynom_add_polynom(a, b):
    if len(a) > len(b):
        return [a[i] + b[i] for i in range(len(b))] + a[len(b):]
    else:
        return [a[i] + b[i] for i in range(len(a))] + b[len(a):]


# Polynomial multiplication function
def polynom_mul_polynom(a, b):
    c = [0] * (len(a) + len(b))
    for i in range(len(a)):
        for j in range(len(b)):
            c[i + j] += a[i] * b[j]
    return c


# The function of dividing a polynomial by a number
def polynom_div_number(a, b):
    return [float(elem) / b for elem in a]


# Determination function of interpolation coefficient
def interpolation_coefficients(x_array, fx_array):
    length = len(fx_array)
    result = [0.0]
    for i in range(length):
        p = [fx_array[i]]
        for j in range(length):
            if i != j:
                t = [-x_array[j], 1.0]
                p = polynom_div_number(polynom_mul_polynom(p, t), x_array[i] - x_array[j])
        result = polynom_add_polynom(result, p)
    return result


# Definition function of interpolation formula
def interpolation_formula(x_array, fx_array, precision=6, output_format='{:+f}*x^{}'):
    coef = [round(elem, precision) for elem in interpolation_coefficients(x_array, fx_array)]
    return ' '.join([output_format.format(coef[i], i) for i in range(len(coef)) if coef[i]])


# Display function of interpolation formula
def print_equation():
    global X, Y
    print('Enter the accuracy of the values (1 to 50, recommended \'6\': it depends on the function): ')
    precision = input_parameter('int')
    while precision < 1 or precision > 50:
        print('#> Invalid input. Repeat again: ')
        precision = input_parameter('int')
    print('Enter display type', '1: regular format (0.001)', '2: exponential format (1E-3): ', ':> ',
          sep='\n', end='')
    format_number = input_parameter('int')
    while format_number < 1 or format_number > 2:
        print('#> Invalid input. Repeat again: ')
        format_number = input_parameter('int')
    format_number = '{:+.' + str(precision) + 'F}*x^{}' if format_number == 1 else '{:+.' + str(precision) + 'E}*x^{}'
    print('f(x) = ', interpolation_formula(X, Y, precision, format_number))


#############################################
#############################################
#############################################
# Logical part 3. Menu
def menu(item):
    global main_step
    if item == '0':
        exit(0)
    elif item == '1':
        add_points()
        main_step = 0
    elif (nSize > 0) and (item == '2'):
        show_points()
    elif (nSize > 1) and (item == '3'):
        cls_points()
        main_step = 0
    elif (nSize > 1) and (item == '4'):
        shell_sort()
        main_step = 1
    elif (nSize > 1) and (main_step == 1) and (item == '5'):
        interpolation()
    elif (nSize > 1) and (main_step == 1) and (item == '6'):
        print_equation()
    else:
        print('Invalid input')


while True:
    print('--------Menu---------')
    print(str(nSize) + ' points.')
    print('1. Add points from the console')
    if nSize > 0:
        print('2. View all points.')
    if nSize > 1:
        print('3. Delete all points')
        print('4. Sort.')
    if main_step == 1:
        print('5. Interpolate a segment.')
        print('6. Define a table function formula.')
    print('---------------------')
    print('0. Exit')
    print('#> ', end='')
    menu(input())
    nSize = len(X)
    print('---------------------')
