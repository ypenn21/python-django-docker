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
