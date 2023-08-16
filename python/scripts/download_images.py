import json
import os
import re

import requests
from imgurpython import ImgurClient
from joblib import Parallel, delayed
from tqdm import tqdm

file_counter = 0


def download_image(url, save_path, id):
    global file_counter
    file_counter += 1
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # get file extension from path
    file_extension = os.path.splitext(save_path)[1]

    file_path = os.path.join('images/', str(id) + '_' + str(file_counter) + file_extension)

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


client_id = 'e9268b0e7fc302f'
client_secret = '8451d38ec95dd42d3b20a893ac0563cd8aa9d1bd'
#
client = ImgurClient(client_id, client_secret)

# load posts_comments_dict.json
with open("posts_comments_dict.json", "r") as f:
    posts_comments_dict = json.load(f)


def download_images_for_post(post):
    try:
        for comment in posts_comments_dict[post]['comments']:
            combined_id = comment['post_id'] + '_' + comment['comment_id']
            # Create folder for each post
            save_folder = 'images/' + combined_id
            reddit_pattern = r'(https?:\/\/(?:preview|i)\.redd\.it\/[a-zA-Z0-9]+(?:\.(?:jpg|jpeg|png|gif))?(?:\?[^\s]+)?)'
            reddit_urls = re.findall(reddit_pattern, comment['body'])
            pattern = r'(https?:\/\/(?:[\w-]+\.)+[a-zA-Z]{2,6}(?:\/[\w\.-]*)*\/?(?:\.(?:jpe?g|png|gif|bmp|webp)))'
            image_urls = re.findall(pattern, comment['body'])
            album_pattern = r'https?:\/\/(?:www\.|i\.|m\.)?imgur\.(?:com|io)(?:\/(?:a|gallery))?\/?([a-zA-Z0-9]+)'
            album_url = re.findall(album_pattern, comment['body'])
            if len(reddit_urls) != 0:
                for i, reddit_url in enumerate(reddit_urls):
                    file_name = os.path.basename(image_urls[i])
                    file_name = file_name.split('?')[0]
                    save_path = os.path.join(save_folder, file_name)
                    download_image(reddit_url, save_path, combined_id)
            elif len(image_urls) != 0:
                # Download images
                for image_url in image_urls:
                    # print(image_url)
                    file_name = os.path.basename(image_url)
                    file_name = file_name.split('?')[0]
                    save_path = os.path.join(save_folder, file_name)
                    download_image(image_url, save_path, combined_id)

            elif len(album_url) != 0:
                try:
                    for album in album_url:
                        album_images = client.get_album_images(album)
                        for image in album_images:
                            file_name = os.path.basename(image.link)
                            save_path = os.path.join(save_folder, file_name)
                            download_image(image.link, save_path, combined_id)
                except Exception as e:
                    download_image("https://i.imgur.com/" + album + ".png", save_path, combined_id)
                    test = ''
    except Exception as e:
        print(e)


Parallel(n_jobs=-1, verbose=10)(
    delayed(download_images_for_post)(post) for post in tqdm(posts_comments_dict)
)
