import random
from typing import List


def get_four_unique_numbers() -> List[int]:
    unique = False
    random_numbers = []
    while unique == False:
        random_number = random.randint(1, 151)
        if random_number not in random_numbers:
            random_numbers.append(random_number)
        if len(random_numbers) == 4:
            unique = True

    return random_numbers