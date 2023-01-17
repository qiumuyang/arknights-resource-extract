import json
import re
from pathlib import Path
from shutil import copyfile as copy

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
    diff = sorted(diff, key=lambda s: not s.startswith('char'))
    key_name_list = [f"{key}\t{character_table_new[key]['name']}" for key in diff]
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

    url1 = 'https://github.com/Kengxxiao/ArknightsGameData/raw/master/zh_CN/gamedata/excel/character_table.json'
    url2 = 'https://github.com/Kengxxiao/ArknightsGameData/raw/master/zh_CN/gamedata/excel/charword_table.json'

    for url in [url1, url2]:
        r = requests.get(url, proxies={'http': 'http://localhost:8001',
                                       'https': 'http://localhost:8001'}, verify=False)
        r.raise_for_status()
        name = url.split('/')[-1]
        with open(json_dir / name, 'wb') as f:
            f.write(r.content)


if __name__ == '__main__':
    download_json()
    update_json()
