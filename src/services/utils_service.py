import random

def generate_random_number(min_value=0, max_value=100):
    """Generates a random integer between min_value and max_value (inclusive).

    Args:
        min_value (int): The minimum value for the random number. Defaults to 0.
        max_value (int): The maximum value for the random number. Defaults to 100.

    Returns:
        int: The generated random number.
    """
    return random.randint(min_value, max_value)

import math

def is_prime(n):
  """
  Checks if a given number is prime.

  Args:
      n: The number to check.

  Returns:
      True if n is prime, False otherwise.
  """
  if n <= 1:
    return False
  if n <= 3:
    return True
  if n % 2 == 0 or n % 3 == 0:
    return False
  i = 5
  while i * i <= n:
    if n % i == 0 or n % (i + 2) == 0:
      return False
    i += 6
  return True

def factorial(n):   

  """
  Calculates the factorial of a non-negative integer.

  Args:
      n: The non-negative integer.

  Returns:
      The factorial of n.
  """
  if n == 0:
    return 1
  else:
    return n * factorial(n - 1)

def gcd(a, b):
  """
  Calculates the greatest common divisor of two integers.

  Args:
      a: The first integer.
      b: The second integer.

  Returns:
      The greatest common divisor of a and b.
  """
  while b:
    a, b = b, a % b
  return a

def lcm(a, b):
  """
  Calculates the least common multiple of two integers.

  Args:
      a: The first integer.
      b: The second integer.

  Returns:
      The least common multiple of a and b.
  """
  return abs(a * b) // gcd(a, b)

def is_perfect_square(n):
  """
  Checks if a given number is a perfect square.

  Args:
      n: The number to check.

  Returns:
      True if n is a perfect square, False otherwise.
  """
  x = int(math.sqrt(n))
  return x * x == n
    
def sum_of_numbers(numbers):
  """
  Calculates the sum of a list of numbers.

  Args:
      numbers: A list of numbers.

  Returns:
      The sum of the numbers in the list.
  """
  total = 0
  for num in numbers:
    total += num
  return total   
