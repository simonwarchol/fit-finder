import json

import praw
import requests
from tqdm import tqdm

client_id = "TEZT5ADVICnEvYURIQhNlw"
client_secret = "4ce2W8qxA3E3q6AjetMjqj_qCRFj_A"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password="Zhtos628",
    user_agent="testscript by u/simonsays440",
    username="simonsays440",
)
posts_dict = {}


def search_waywt_posts(subreddit, query, before_days, after_days):
    global posts_dict
    url = "https://api.pushshift.io/reddit/search/submission"
    params = {
        "title": query,
        "subreddit": subreddit,
        "before": str(before_days) + 'd',
        "after": str(after_days) + 'd',
    }
    response = requests.get(url, params=params)
    data = response.json()
    for post in data['data']:
        posts_dict[post['id']] = {'title': post['title'],
                                  'post_id': post['id'],
                                  'score': post['score'],
                                  'created_utc': post['created_utc'],
                                  'link': post['permalink']}

    #     Write to posts dict
    with open("posts_dict.json", "w") as f:
        json.dump(posts_dict, f, indent=4)


def get_posts():
    subreddit = "malefashionadvice"
    query = "WAYWT"
    #
    for i in tqdm(range(0, 4000, 50)):
        search_waywt_posts(subreddit, query, i, i + 50)


def get_comments(submission_id):
    post = reddit.submission(id=submission_id)
    comment_list = []
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        comment_list.append({'body': comment.body,
                             'comment_id': comment.id,
                             'post_id': post.id,
                             'author': str(comment.author),
                             'score': comment.score,
                             'created_utc': comment.created_utc,
                             'link': comment.permalink})
    return comment_list


if __name__ == "__main__":
    #     get_posts()
    with open("posts_dict.json", "r") as f:
        submissions_dict = json.load(f)
    for post in tqdm(submissions_dict):
        submissions_dict[post]['comments'] = get_comments(post)

    with open("posts_comments_dict.json", "w") as f:
        json.dump(submissions_dict, f, indent=4)