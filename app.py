from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
import logging
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import praw
import time
import os
import config
from data import get_comments_word_count
# import pandas as pd


app = Flask(__name__, static_folder=config.static_folder, static_url_path=config.static_url_path)
bootstrap = Bootstrap(app)

app.secret_key = config.SECRET_KEY

reddit = praw.Reddit(client_id=config.client_id,
                     client_secret=config.client_secret,
                     user_agent=config.user_agent)

logging.basicConfig(filename='example.log', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

no_comments = 500#maximum is 1000 but fetches ~800


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/', methods=['GET', 'POST'])
def index():
    start_for_total = time.time()
    start = time.time()

    # comments = (x.body for x in reddit.subreddit('all').stream.comments())
    comments = [x.body for x in reddit.subreddit('all').comments(limit=no_comments)]#TODO: no_comments twice
    output = get_comments_word_count(comments, no_comments)
    logging.info("getting %s comments; time - %s", no_comments, time.time() - start)

    start = time.time()
    output2 = output.copy()
    for key, value in output2.items():
        if key in STOPWORDS:
            del output[key]
    del output2
    logging.info('%s words left after removing stopwords; time - %s', len(output.keys()), time.time() - start)

    start = time.time()
    wc = WordCloud(background_color='white').generate_from_frequencies(output)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(config.static_folder, 'new_plot.png'))
    plt.clf()
    logging.info('drawing figure time - %s', time.time() - start)

    time_taken = time.time() - start_for_total
    logging.info('total time - %s', time_taken)

    return render_template('index.html', name='word cloud', time_taken=time_taken, cache=-1)


if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.port)
