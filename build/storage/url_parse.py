import json
import re

pattern = r'^(?!.*\.\w{2,4}$).*$'

# urls_without_file_extension = [url for url in urls if re.match(pattern, url)]

with open("urls.json", "r") as f:
    urls = json.load(f)

i = 0
new_dict = {}
for k, v in urls.items():
    match = re.match(pattern, v['url'])
    # Check if k['url'] contains "preview.redd.it
    test = v['url'].find("preview.redd.it")

    if match is not None and test == -1:
        cleaned_url = re.sub(r'[\?#].*', '', v['url'])
        v['url'] = cleaned_url
    new_dict[k] = v

# Save new_dict to a file
with open("urls_cleaned.json", "w") as f:
    json.dump(new_dict, f, indent=4)