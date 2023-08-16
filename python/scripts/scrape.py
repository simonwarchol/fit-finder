import datetime
import json

import praw

client_id = "TEZT5ADVICnEvYURIQhNlw"
client_secret = "4ce2W8qxA3E3q6AjetMjqj_qCRFj_A"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password="Zhtos628",
    user_agent="testscript by u/simonsays440",
    username="simonsays440",
)

posts = {}

subreddit = reddit.subreddit("malefashionadvice")


def fetch_comments(post_id):
    post = reddit.submission(id=post_id)
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        id = post.id + '_' + comment.id
        posts[id] = {'body': comment.body,
                     'comment_id': comment.id,
                     'post_id': post.id,
                     'author': str(comment.author),
                     'score': comment.score,
                     'created_utc': comment.created_utc,
                     'link': comment.permalink}


total_list = []

# LOAD LIST FROM total_list.json
# with open("total_list.json", "r") as f:
#     total_list = json.load(f)

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False

# Remove non-serializable objects from the dictionary


i = 0
while True:
    i += 1
    if len(total_list) == 0:
        sub_gen = subreddit.search("WAYWT", sort="new", limit=1000)
    else:
        sub_gen = subreddit.search("WAYWT", sort="new", limit=1000)

        # sub_gen = subreddit.search("WAYWT", sort="new", limit=1000, params={"after": total_list[-1]})
    for submission in sub_gen:
        print(submission.title)
        if submission.title.startswith("WAYWT"):
            print(f" {str(i)} Post title: {submission.title}")
            date_str = datetime.datetime.fromtimestamp(submission.created_utc)
            total_list.append(submission.fullname)
            print(f" {str(i)} Post Date: {date_str}")
            fetch_comments(submission.id)
    with open("search_comments_data.json", "w") as f:
        json.dump(posts, f, indent=4)
    with open("total_list.json", "w") as f:
        json.dump(total_list, f, indent=4)

