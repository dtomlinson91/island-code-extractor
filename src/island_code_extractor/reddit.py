import sys
from typing import List, Union
from pprint import pprint

import pendulum
import praw
from praw.models import Submission, Comment, MoreComments

from . import panaetius
from . import CONFIG


top_level_comments = []


def get_reddit_instance() -> praw.Reddit:
    return praw.Reddit(
        client_id=CONFIG.reddit_id,
        client_secret=CONFIG.reddit_secret,
        user_agent=CONFIG.reddit_user_agent,
    )


def get_comments_from_thread(
    delta: int = -1,
    depth: int = -1,
    sort: str = "new",
    relative: Union[int, float, str] = "now",
) -> List[Comment]:

    reddit_instance = get_reddit_instance()
    return get_top_level_comments(
        reddit_instance=reddit_instance,
        delta=delta,
        depth=depth,
        sort=sort,
        relative=relative,
    )


def get_top_level_comments(
    reddit_instance: praw.Reddit,
    delta: int,
    depth: int,
    sort: str,
    relative: Union[int, float, str] = "now",
) -> List[Comment]:

    if delta < -1:
        logger.error(f"Negative time delta {delta}.")
        sys.exit(1)
    # total_comments = []
    submission = reddit_instance.submission(id=CONFIG.reddit_thread_id)
    submission.comment_sort = sort
    get_more_comments(
        submission.comments.list(),
        delta=delta,
        depth=depth,
        relative=relative,
        sort=sort,
    )
    total_comments = [
        i
        for i in top_level_comments
        if ((_check_time(i, delta=delta) or delta != -1) and not i.stickied)
    ]
    # return None
    return total_comments


def get_more_comments(
    comments_obj: Union[Comment, MoreComments],
    delta: int,
    depth: int,
    sort: str,
    relative: Union[int, float, str] = "now",
) -> None:

    for i in comments_obj:
        if i.depth > depth:
            continue
        if isinstance(i, Comment):
            if i.stickied:
                continue
            if _check_time(i, delta=delta, relative=relative):
                top_level_comments.append(i)
            else:
                # if fails the timecheck.
                if sort in ["new", "old"]:
                    # if sorted by time, break to stop further api calls.
                    break
                # if not sorted by time, keep going
                continue
        elif isinstance(i, MoreComments):
            print(".")
            get_more_comments(i.comments(), delta=delta, depth=depth, sort=sort)

def _check_time(
    comment: Comment, delta: int, relative: Union[int, float, str] = "now"
) -> bool:
    # delta =-1 functionality needs adding
    if relative == "now":
        current_time = pendulum.now("Europe/London")
    elif relative == "submission":
        current_time = pendulum.from_timestamp(comment.submission.created_utc)
    else:
        current_time = pendulum.from_timestamp(relative)
    comment_time = pendulum.from_timestamp(comment.created_utc)
    return current_time.diff(comment_time).in_seconds() <= delta

