import re
from collections import deque, Counter


def get_first_comments(reddit, no_comments):
    """
    Produces first Counter of words in selected comments to create deque which will be updated further
    :param reddit: connection to reddit comment streaming
    :param no_comments: how many comments to use a starting point for deque (analysis pool);
                        time can be added if the last if modified/another added
    :return: counter of words from (over) no_comments
    """

    output = Counter()

    ## Approach with list appending (1/3)
    # start_comments = []
    # len_words_start = 0

# for i, comment in enumerate(reddit.subreddit('all').stream.comments()):
    for i, comment in enumerate(reddit.subreddit('all').stream.comments()):


        # print([re.sub("[^a-zA-Z]+", "", j) for j in comment.body.split(' ')])#TODO: usunac '' - czyli nic..
        # print(len(output))
        # print(output)
        output += Counter([re.sub("[^a-zA-Z]+", "", k) for k in comment.body.split(' ')])

        if no_comments == i:
            break

    ## Approach with list appending (2/3)
    # print(comment.body.split(' '))
    # [re.sub("[^a-zA-Z]+", "", i) for i in comment.body.split(' ')]
    # len_words_start = len_words_start + len([re.sub("[^a-zA-Z]+", "", i) for i in comment.body.split(' ')])
    # print(len_words_start)

    ## List appending only here(3/3)
    # start_comments.append([re.sub("[^a-zA-Z]+", "", i) for i in comment.body.split(' ')])
    # print (start_comments[i])

    return output




