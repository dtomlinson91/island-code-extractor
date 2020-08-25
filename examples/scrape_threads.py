import csv
import json

from island_code_extractor import CONFIG
from island_code_extractor import process
from island_code_extractor import panaetius
from island_code_extractor import reddit


def save_json():
    praw_comments = reddit.get_comments_from_thread(delta=68400, depth=1, sort="new")
    dream_code_data = process.get_comment_data(praw_comments)
    print(len(dream_code_data))
    # with open(
    #     f"{panaetius.CONFIG.output_path}/dream_codes_i0ey19_310720x_0215.json", "w+"
    # ) as output:
    #     json.dump(dream_code_data, output, indent=2)


def save_csv():
    praw_comments = reddit.get_comments_from_thread(
        delta=60 * 60 * 24 * 20, depth=0, sort="top", relative="submission"
    )
    dream_code_data = process.get_comment_data(praw_comments)
    panaetius.logger.info("Saving csv.")
    headers = list(dream_code_data[0].keys())
    with open(f"{CONFIG.reddit_output_path}/test.csv", "w+") as output:
        writer = csv.DictWriter(output, fieldnames=headers)
        writer.writeheader()
        for data in dream_code_data:
            writer.writerow(data)


if __name__ == "__main__":
    # save_json()
    save_csv()
