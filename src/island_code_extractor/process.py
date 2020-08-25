from typing import List, Dict
import re

from praw.models import Comment


def _extract_time(comment_instance: Comment) -> str:
    return comment_instance.created_utc


def _extract_body(comment_instance: Comment) -> str:
    return comment_instance.body


def _extract_user(comment_instance: Comment) -> str:
    try:
        return comment_instance.author.name
    except AttributeError:
        return "deleted"


def _extract_permalink(comment_instance: Comment) -> str:
    return f"https://reddit.com{comment_instance.permalink}"


def _extract_dream_code(comment_instance: Comment) -> str:
    dream_address_re = r"(DA(?:\-[0-9]{4}){3})"
    if match := re.search(dream_address_re, comment_instance.body, re.IGNORECASE):
        return match.group(1)
    return False


def _extract_country(comment_instance: Comment) -> str:
    pass


def _extract_keywords(comment_instance: Comment) -> str:
    pass


def get_comment_data(praw_comments: List[Comment]) -> List[Dict]:
    """
    Return data from comments.

    Args:
        praw_comments (List[Comment]): A list containing praw `Comment` objects.

    Returns:
        List[Dict]: A list of the properties of a comment.
    """
    return [
        dict(
            [
                ("time", _extract_time(comment)),
                ("body", _extract_body(comment)),
                ("user", _extract_user(comment)),
                ("permalink", _extract_permalink(comment)),
                # ("dream_code", _extract_dream_code(comment)),
            ]
        )
        for comment in praw_comments
        # if _extract_dream_code(comment) is not False
    ]
