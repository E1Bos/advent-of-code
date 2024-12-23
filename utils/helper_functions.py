import re
from typing import Any, Iterable


# region String Processing
def split_groups(text: str) -> list[list[str]]:
    """
    Splits the given text into groups based on double newline separators and returns a list of lists of strings.

    Each group of text is split into individual lines, which are then stored as lists within the main list.

    Args:
        text (str): The text to be split into groups.

    Returns:
        list[list[str]]: A list of lists where each inner list contains the lines of a group.

    Example:
        >>> split_groups("Group 1 line 1\nGroup 1 line 2\n\nGroup 2 line 1")
        [['Group 1 line 1', 'Group 1 line 2'], ['Group 2 line 1']]
    """
    return [group.strip().splitlines() for group in text.split("\n\n") if group.strip()]

def comma_separated(text: str) -> list[str]:
    """
    Extracts all comma-separated substrings from the given text and returns them as a list of strings.

    Args:
        text (str): The text from which to extract comma-separated substrings.

    Returns:
        list[str]: A list of strings extracted from the given text.

    Example:
        >>> comma_separated("one, two, three,four, five")
        ['one', 'two, 'three', 'four', 'five']
    """
    return [s.strip() for s in text.split(",")]

def extract_words(text: str) -> list[str]:
    """
    Extracts all words from the given text and returns them as a list of strings.

    Args:
        text (str): The text from which to extract words.

    Returns:
        list[str]: A list of strings extracted from the given text.

    Example:
        >>> extract_words("There are two apples and five oranges.")
        ['There', 'are', 'two', 'apples', 'and', 'five', 'oranges']
    """
    return re.findall(r"\w+", text)


def extract_numbers(text: str) -> list[int]:
    """
    Extracts all numbers from the given text and returns them as a list of integers.

    Args:
        text (str): The text from which to extract numbers.

    Returns:
        list[int]: A list of integers extracted from the given text.

    Example:
        >>> extract_numbers("There are 2 apples and 5 oranges.")
        [2, 5]
    """
    return list(map(int, re.findall(r"\d+", text)))


def extract_numbers_with_signs(text: str) -> list[int]:
    """
    Extracts all numbers from the given text and returns them as a list of integers.

    Args:
        text (str): The text from which to extract numbers.

    Returns:
        list[int]: A list of integers extracted from the given text.

    Example:
        >>> extract_numbers("There are 2 apples and 5 oranges.")
        [2, 5]
    """
    return list(map(int, re.findall(r"[-+]?\d+", text)))

def extract_numbers_to_string(text: str) -> str:
    """
    Extracts all numbers from the given text and returns them as a string.

    Args:
        text (str): The text from which to extract numbers.

    Returns:
        str: A string containing all numbers extracted from the given text.

    Example:
        >>> extract_numbers("There are 2 apples and 5 oranges.")
        "2 5"
    """
    return "".join(re.findall(r"\d+", text))
    

def find_in_grid(grid: list[list[Any]], target: Any) -> tuple[int, int] | None:
    """
    Finds the first occurrence of a target in a 2D grid of strings and returns its position as a tuple of integers (row, col).

    Args:
        grid (list[list[Any]]): The 2D grid of strings to search in.
        target (Any): The target string to search for.

    Returns:
        tuple[int, int] | None: The position of the target in the grid as a tuple of two integers (row, col), or None if the target is not found.

    Example:
        >>> find_in_grid([['a', 'b'], ['c', 'd']], 'c')
        (1, 0)
    """
    for i, row in enumerate(grid):
        if target in row:
            return i, row.index(target)
    return None

def outside_grid(grid: list[list[Any]] | tuple[int, int] | int, row: int, col: int) -> bool:
    if isinstance(grid, int):
        return row < 0 or col < 0 or row >= grid or col >= grid
    
    if isinstance(grid, tuple):
        return row < 0 or col < 0 or row >= grid[0] or col >= grid[1]
    
    if isinstance(grid, list):
        return row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0])
    
    raise TypeError("Grid must be a list or tuple")


# def is_outside_grid(grid: list[list[Any]], row: int, col: int) -> bool:
    # return row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0])


def find_in_grid_or_error(grid: list[list[Any]], target: Any) -> tuple[int, int]:
    """
    Finds the first occurrence of a target in a 2D grid of strings and returns its position as a tuple of integers (row, col).

    Args:
        grid (list[list[Any]]): The 2D grid of strings to search in.
        target (Any): The target string to search for.

    Returns:
        tuple[int, int]: The position of the target in the grid as a tuple of two integers (row, col).

    Raises:
        ValueError: If the target is not found in the grid.

    Example:
        >>> find_in_grid_or_error([['a', 'b'], ['c', 'd']], 'c')
        (1, 0)
    """
    pos = find_in_grid(grid, target)
    if pos is None:
        raise ValueError(f"Target {target} not found in grid")
    return pos


def is_palindrome(text: str) -> bool:
    """
    Checks if the given string is a palindrome.

    Args:
        text (str): The string to be checked.

    Returns:
        bool: True if the string is a palindrome, False otherwise.

    Example:
        >>> is_palindrome("racecar")
        True
        >>> is_palindrome("hello")
        False
    """
    return text == text[::-1]


def char_frequency(text: str) -> dict[str, int]:
    """
    Returns a dictionary where the keys are the unique characters in the given text and the values are their respective frequencies.

    Args:
        text (str): The string to be processed.

    Returns:
        dict[str, int]: A dictionary mapping each character to its frequency in the given text.

    Example:
        >>> char_frequency("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    return {char: text.count(char) for char in text}


def lmap(func, *iterables):
    return list(map(func, *iterables))


# region Numbers


def greatest_common_divisor(a: int, b: int) -> int:
    """
    Calculates the greatest common divisor (GCD) of two integers.

    The GCD of two integers a and b is the largest positive integer that
    divides both a and b without leaving a remainder. This function computes
    it using the Euclidean algorithm, which involves repeated division and
    remainder calculations.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The greatest common divisor of the two integers.

    Example:
        >>> greatest_common_divisor(48, 18)
        6
    """
    while b != 0:
        a, b = b, a % b
    return a


def least_common_multiple(a: int, b: int) -> int:
    """
    Calculates the least common multiple (LCM) of two integers.

    The LCM of two integers a and b is the smallest positive integer that is
    divisible by both a and b. This function computes it using the formula:
    LCM(a, b) = (a * b) / GCD(a, b), where GCD is the greatest common divisor.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The least common multiple of the two integers.

    Example:
        >>> least_common_multiple(4, 6)
        12
    """
    return a * b // greatest_common_divisor(a, b)


def prime_factors(n: int) -> list[int]:
    """
    Finds all prime factors of a given number.

    A prime factor is a prime number that divides the given number without
    leaving a remainder. This function finds all such numbers by testing
    divisibility from 2 up to the square root of the number.

    Args:
        n (int): The number to find prime factors of.

    Returns:
        list[int]: The list of prime factors of the given number.

    Example:
        >>> prime_factors(12)
        [2, 2, 3]
    """

    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors


def is_prime(n: int) -> bool:
    """
    Checks if a number is prime.

    A prime number is a natural number greater than 1 that is not a product
    of two smaller natural numbers. This function checks if the given number
    is prime by testing divisibility from 2 up to the square root of the
    number.

    Args:
        n (int): The number to check for primality.

    Returns:
        bool: True if the number is prime, False otherwise.

    Example:
        >>> is_prime(11)
        True
        >>> is_prime(4)
        False
    """
    if n <= 1 or (n > 2 and n % 2 == 0):
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def modular_inverse(a: int, m: int) -> int:
    """
    Calculates the modular inverse of a modulo m.

    The modular inverse of a number 'a' is a number 'x' such that the equation
    a*x = 1 (mod m) is satisfied.

    Args:
        a (int): The number of which the modular inverse is to be calculated.
        m (int): The modulus.

    Returns:
        int: The modular inverse of a modulo m.

    Example:
        >>> modular_inverse(2, 5)
        3
    """
    return pow(a, m - 2, m)


# region Matrix


def parse_grid(text: Iterable[str]) -> list[list[str]]:
    """
    Parses the given text into a 2D list of integers.

    Args:
        text (str): The text to be parsed into a 2D list of strings.

    Returns:
        list[list[str]]: A 2D list of integers parsed from the given text.

    Example:
        >>> parse_grid("1 2 3\n4 5 6")
        [['1', '2', '3'], ['4', '5', '6']]
    """
    return [list(row.split()) for row in text]


def gridify(text: list[str]) -> list[list[str]]:
    return [[col for col in row] for row in text]


def gridify_ints(text: list[str]) -> list[list[int]]:
    return [[int(col) for col in row] for row in text]


def rotate_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotates the given square matrix 90 degrees clockwise in place.

    Args:
        matrix (list[list[int]]): A 2D list representing the square matrix to be rotated.

    Returns:
        list[list[int]]: The matrix after being rotated 90 degrees clockwise.

    Example:
        >>> rotate_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    """
    n = len(matrix)
    for i in range(n // 2):
        for j in range(i, n - i - 1):
            temp = matrix[i][j]
            matrix[i][j] = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - 1 - j]
            matrix[n - 1 - i][n - 1 - j] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = temp
    return matrix


def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:
    """
    Transposes the given matrix.

    Args:
        matrix (list[list[int]]): A 2D list representing the matrix to be transposed.

    Returns:
        list[list[int]]: The transposed matrix.

    Example:
        >>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    return [list(row) for row in zip(*matrix)]


def find_adjacent(matrix: list[list[int]], row: int, col: int) -> list[tuple[int, int]]:
    """
    Finds all adjacent cells in the given matrix.

    Args:
        matrix (list[list[int]]): A 2D list representing the matrix to search in.
        row (int): The row of the cell to search from.
        col (int): The column of the cell to search from.

    Returns:
        list[tuple[int, int]]: A list of all adjacent cells (up, down, left, right) as tuples of (row, col).

    Example:
        >>> find_adjacent([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 1)
        [(0, 1), (2, 1), (1, 0), (1, 2)]
    """
    adjacent = []
    if row > 0:
        adjacent.append((row - 1, col))
    if row < len(matrix) - 1:
        adjacent.append((row + 1, col))
    if col > 0:
        adjacent.append((row, col - 1))
    if col < len(matrix[0]) - 1:
        adjacent.append((row, col + 1))
    return adjacent


def system_of_equation(
    eq1: tuple[int, int] | list[int],
    eq2: tuple[int, int] | list[int],
    goal: tuple[int, int] | list[int],
) -> tuple[int, int] | None:
    """
    Solves a system of linear equations with two variables.

    Args:
        eq1 (tuple[int, int] | list[int]): The coefficients of the first equation.
        eq2 (tuple[int, int] | list[int]): The coefficients of the second equation.
        goal (tuple[int, int] | list[int]): The right-hand side of both equations.

    Returns:
        tuple[int, int] | None: The solution as a tuple of two integers, or None if no solution exists.

    Example:
        >>> system_of_equation((2, 2), (3, 5), (8, 12))
        (1, 2)
    """
    det = eq1[0] * eq2[1] - eq1[1] * eq2[0]

    if det == 0:
        return None

    a = (goal[0] * eq2[1] - goal[1] * eq2[0]) // det
    b = (eq1[0] * goal[1] - eq1[1] * goal[0]) // det

    if a < 0 or b < 0:
        return None

    if eq1[0] * a + eq2[0] * b == goal[0] and eq1[1] * a + eq2[1] * b == goal[1]:
        return (a, b)
    return None


def print_grid(grid: list[list[Any]]):
    print("\n".join("".join(str(x) for x in row) for row in grid))
