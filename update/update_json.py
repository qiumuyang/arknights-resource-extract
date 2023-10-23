from __future__ import annotations

import json
import re
from pathlib import Path
from shutil import copyfile as copy

from tqdm import tqdm

OLD_CHAR_PATH = Path('excel/character_table.json')
OLD_WORD_PATH = Path('excel/charword_table.json')
NEW_CHAR_PATH = Path('excel/new/character_table.json')
NEW_WORD_PATH = Path('excel/new/charword_table.json')


def update_json():
    with open(OLD_CHAR_PATH, encoding='utf8') as f:
        character_table: dict = json.load(f)

    with open(NEW_CHAR_PATH, encoding='utf8') as f:
        character_table_new: dict = json.load(f)

    # diff the char keys
    old_keys = set(character_table.keys())
    new_keys = set(character_table_new.keys())

    diff = sorted(new_keys.difference(old_keys),
                  key=lambda s: int(re.search(r'\d+', s).group(0)))
    diff: list[str] = sorted(diff, key=lambda s: not s.startswith('char'))
    key_name_list = [
        f"{key:<35}{character_table_new[key]['name']}" for key in diff
    ]
    msg = '\n'.join(key_name_list)

    if diff:
        with open('update.txt', 'w', encoding='utf8') as f:
            print(msg)
            print(msg, file=f)

        input('Overwrite existing json?'
              '[Press Any Key]')

        copy(NEW_CHAR_PATH, OLD_CHAR_PATH)
        copy(NEW_WORD_PATH, OLD_WORD_PATH)
    else:
        print('No update')
    return diff


def download_json():
    import requests
    import urllib3
    from urllib3.exceptions import InsecureRequestWarning

    urllib3.disable_warnings(InsecureRequestWarning)

    json_dir = Path('excel/new')
    json_dir.mkdir(exist_ok=True)
    old_dir = Path('excel/old')
    old_dir.mkdir(exist_ok=True)

    # url1 = 'https://github.com/Kengxxiao/ArknightsGameData/raw/master/zh_CN/gamedata/excel/character_table.json'
    # url2 = 'https://github.com/Kengxxiao/ArknightsGameData/raw/master/zh_CN/gamedata/excel/charword_table.json'
    url1 = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
    url2 = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/charword_table.json"

    for url in [url1, url2]:
        r = requests.get(url,
                         proxies={
                             'http': 'http://localhost:7890',
                             'https': 'http://localhost:7890'
                         },
                         verify=False,
                         stream=True)
        name = url.split('/')[-1]
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024 * 256 # 256KB
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(json_dir / name, 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()

        existing = Path('excel') / name
        if existing.exists():
            copy(existing, old_dir / name)


if __name__ == '__main__':
    download_json()
    update_json()
