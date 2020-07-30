# from pprint import pprint
from typing import List, Tuple

import pendulum
import praw
from praw.models import Submission, Comment

from island_code_extractor import panaetius


def get_reddit_instance() -> praw.Reddit:
    return praw.Reddit(
        client_id=panaetius.CONFIG.reddit_id,
        client_secret=panaetius.CONFIG.reddit_secret,
        user_agent=panaetius.CONFIG.reddit_user_agent,
    )


def get_hourly_comments(reddit_instance: praw.Reddit) -> List[Comment]:
    total_comments = []
    submission = reddit_instance.submission(id=panaetius.CONFIG.reddit_thread_id)
    submission.comment_sort = "new"
    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        if _check_hour(top_level_comment):
            total_comments.append(top_level_comment)
        else:
            break
    return total_comments


def _check_hour(comment: Submission):
    current_time = pendulum.now("Europe/London")
    comment_time = pendulum.from_timestamp(comment.created_utc)
    return current_time.diff(comment_time).in_seconds() <= 3600


if __name__ == "__main__":
    reddit = get_reddit_instance()
    comments = get_hourly_comments(reddit)
    print(dir(comments[0]))
