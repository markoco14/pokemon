import os
import random
from typing import List

from dotenv import load_dotenv

load_dotenv()


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


def get_s3_domain():
    aws_bucket = os.environ.get("S3_BUCKET")
    aws_region = os.environ.get("AWS_DEFAULT_REGION")
    return f"https://{aws_bucket}.s3.{aws_region}.amazonaws.com"


def to_public_word(word_row) -> dict:
    word = dict(word_row)
    word["large_img_path"] = f'{get_s3_domain()}/{word["large_img_path"]}'
    word["thumbnail_img_path"] = f'{get_s3_domain()}/{word["thumbnail_img_path"]}'
    return word