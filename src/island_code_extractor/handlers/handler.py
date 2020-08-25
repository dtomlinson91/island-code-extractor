"""
Run this file from `./src` with `poetry run python -m island_code_extractor.handlers.handler`
"""

import csv
import json

from .. import CONFIG
from .. import process
from .. import panaetius
from .. import reddit


def save_csv():
    praw_comments = reddit.get_comments_from_thread(
        delta=60 * 60 * 24 * 20, depth=0, sort="top", relative="submission"
    )
    dream_code_data = process.get_comment_data(praw_comments)
    panaetius.logger.info("Saving CSV File")
    headers = list(dream_code_data[0].keys())

    with open(f"{CONFIG.reddit_output_path}/test.csv", "w+") as output:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for data in dream_code_data:
            writer.writerow(data)


if __name__ == "__main__":
    save_csv()
