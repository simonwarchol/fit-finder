import json
import glob
from tqdm import tqdm
import re
from joblib import Parallel, delayed

master_comments = {}

# Load Comments.json
with open("comments.json", "r") as f:
    comments = json.load(f)

with open("index_mapping.json", "r") as f:
    index_mapping = json.load(f)

def remove_trailing_underscore_and_digits(s):
    return re.sub(r'(_\d+)$', '', s)

def remove_img(s):
    return re.sub(r'^(../img/)', '', s)

def process_item(key, value):
    files = glob.glob(f"../img/{value}*")
    if len(files) == 1:
        trimmed_filename = remove_img(files[0])
        comment_id = remove_trailing_underscore_and_digits(value)
        comment_data = comments[comment_id]
        comment_data['filename'] = trimmed_filename
        return value, comment_data
    else:
        print(f"Error: {value} has {len(files)} files")
        return None

# Use joblib.Parallel and tqdm to parallelize the for loop with a progress bar
num_cores = -1  # Use all available cores
results = Parallel(n_jobs=num_cores)(
    delayed(process_item)(key, value) for key, value in tqdm(index_mapping.items())
)

# Filter out any None results and convert the results to a dictionary
master_comments = {k: v for k, v in results if k is not None}

with open("master_comments.json", "w") as f:
    json.dump(master_comments, f, indent=4)