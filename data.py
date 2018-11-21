import re
from collections import Counter


class TooFewCommentsError(Exception):
    pass


def get_comments_word_count(comments, no_comments=100):
    """
    Creates a Counter that is updated with words from comments
    :param comments: list of strings (comments);
    :param no_comments:#TODO: no_comments twice
    :return: counter of words from
    """

    if no_comments < 1:
        raise TooFewCommentsError()

    output = Counter()

    for i, comment in enumerate(comments):

        if no_comments == i:
            break

        split_comment = comment.split(' ')
        comment_counts = [re.sub("[^a-zA-Z]+", "", k) for k in split_comment]
        output.update(comment_counts)

    del output['']

    return output




