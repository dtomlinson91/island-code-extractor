from praw.models import Comment

import island_code_extractor
from island_code_extractor import reddit


def _extract_time(comment: Comment) -> str:
    return comment.created_utc


def _extract_body(comment: Comment) -> str:
    return comment.body


def _extract_user(comment: Comment) -> str:
    return comment.author


def _extract_permalink(comment: Comment) -> str:
    return comment.permalink


def _extract_code(comment: Comment) -> str:
    pass


def _extract_country(comment: Comment) -> str:
    pass


def _extract_keywords(comment: Comment) -> str:
    pass


if __name__ == "__main__":
    reddit_instance = reddit.get_reddit_instance()
    comments = reddit.get_hourly_comments(reddit_instance)
    for comment in comments:
        print(_extract_permalink(comment))

