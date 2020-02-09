#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
File with functions for working with Lagrange interpolation.
Main features to use:
- point_interpolation(). Used to interpolate a point.
- interpolation_coeffients(). Used to determine interpolation coefficients.
- interpolation_formula(). Function that returns a polynomial as a string for input data.
"""


def point_interpolation(x_array, fx_array, nStart, nStop, x):
    """
    Interpolation of a single point by the Lagrange method.
    :param x_array: Array with X coordinates.
    :param fx_array: Array with Y coordinates.
    :param nStart: Index of the point at which the interpolation begins
    :param nStop: Index of the point at which the interpolation ends
    :param x: X coordinate for interpolation
    :return: Y coordinate - the result of the interpolation
    """
    number_type = type(x_array[0]) if x_array else type(fx_array[0]) if fx_array else type(x)
    ntResult = number_type(0)
    for i in range(nStart, nStop):
        ntProduct = fx_array[i]
        for j in range(nStart, i):
            ntProduct *= (x - x_array[j]) / (x_array[i] - x_array[j])
        for j in range(i + 1, nStop):
            ntProduct *= (x - x_array[j]) / (x_array[i] - x_array[j])
        ntResult += ntProduct
    return ntResult


def polynomial_add_polynomial(a, b):
    """
    Addition function of two polynomials.
    :param a: First polynomial.
    :param b: Second polynomial.
    :return: The result of adding two polynomials
    """
    len_a, len_b = len(a), len(b)
    if len_a < len_b:
        a, b, len_a, len_b = b, a, len_b, len_a
    return [a[i] + b[i] for i in range(len_b)] + a[len_b:]


def polynomial_mul_polynomial(a, b):
    """
    Multiplication function of two polynomials.
    :param a: First polynomial.
    :param b: Second polynomial.
    :return: The result of multiplication two polynomials
    """
    number_type = type(a[0]) if a else type(b[0]) if b else float
    len_a, len_b = len(a), len(b)
    c = [number_type(0)] * (len_a + len_b)
    for i in range(len_a):
        for j in range(len_b):
            c[i + j] += a[i] * b[j]
    return c


def polynomial_div_number(a, number):
    """
    The function of dividing a polynomial by a number.
    :param a: Polynomial.
    :param number: The number to divide by.
    :return: The result of dividing the polynomial by a number.
    """
    return [elem / number for elem in a]


def interpolation_coefficients(x_array, fx_array):
    """
    Function for finding coefficients of the Lagrange polynomial.
    :param x_array: Array of X coordinates
    :param fx_array: Array of F(X) coordinates
    :return: Coefficients of the Lagrange polynomial as a list
    """
    number_type = type(x_array[0]) if x_array else type(fx_array[0]) if fx_array else float
    fx_length = len(fx_array)
    result = [number_type(0)]
    for i in range(fx_length):
        p = [fx_array[i]]
        for j in range(0, i):
            p = polynomial_div_number(polynomial_mul_polynomial(p, [-x_array[j], number_type(1)]),
                                      x_array[i] - x_array[j])
        for j in range(i + 1, fx_length):
            p = polynomial_div_number(polynomial_mul_polynomial(p, [-x_array[j], number_type(1)]),
                                      x_array[i] - x_array[j])
        result = polynomial_add_polynomial(result, p)
    return result


def interpolation_formula(x_array, fx_array, rounded_accuracy, format_number=None):
    """
    Function that returns a polynomial as a string for input data
    :param x_array: Array of X coordinates
    :param fx_array: Array of F(X) coordinates
    :param rounded_accuracy: A number that is rounded with precision
    :param format_number: Format of numbers in a string (optional)
    :return: A Lagrange polynomial as a string
    """
    coefficients = [round(i, rounded_accuracy) for i in interpolation_coefficients(x_array, fx_array)]
    output_format = format_number or ('{:+.' + str(rounded_accuracy) + 'f}*x^{}')
    s = ' '.join(output_format.format(coefficients[i], i) for i in range(len(coefficients)) if coefficients[i])
    return s or output_format.format(0, 0)
