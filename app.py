from flask import Flask, render_template, url_for
from data import get_first_comments
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import praw
import time
import os
import config


# app = Flask(__name__, static_folder='/home/piotrek/PycharmProjects/reddit_playground/static',
#             static_url_path='/home/piotrek/PycharmProjects/reddit_playground/static')
app = Flask(__name__)#, static_folder='static', static_url_path='/static')

# app.config['SECRET_KEY'] = 'hard to guess string'
app.config.from_object('config')

reddit = praw.Reddit(client_id=app.config['client_id'],
                     client_secret=app.config['client_secret'],
                     user_agent=app.config['user_agent'])

#set no of comments (deque size);;; time also might be used if changed if/break in the get_first comments
no_comments = 100


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
    start = time.time()
    output = get_first_comments(reddit, no_comments)
    print("{} - to get {} comments".format(time.time() - start, no_comments))
    start = time.time()
    print(no_comments)
    print('output and len')
    print(output)
    print(len(output.keys()))
    print('stopwords:')
    print(STOPWORDS)
    output2 = output.copy()
    for key, value in output2.items():
        if key in STOPWORDS:
            # print(key)
            del output[key]
        #     pass
        # else:
        #     output2[key] = value
    del output['']
    print('{} len(output) after cleaning that took {} ;;; output:'.format(len(output.keys()), time.time() - start))
    print(output)
    start = time.time()
    wc = WordCloud().generate_from_frequencies(output)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('/home/piotrek/PycharmProjects/reddit_playground/static/new_plot.png')
    plt.clf()
    print('_________________')
    print("{} - to draw a figure".format(time.time() - start))

    return render_template('index.html', name='word cloud', cache=-1)
                           # url='/home/piotrek/PycharmProjects/reddit_playground/static/new_plot.png')


if __name__ == '__main__':
    app.run(debug=True)