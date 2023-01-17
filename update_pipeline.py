from pathlib import Path

from table import Table
from update.extract_apk import extract_all, clean_all
from update.update_avatar import update_avatar
from update.update_json import update_json, download_json
from update.update_portrait import update_portrait


def tick(key, container):
    return '✓' if key in container else ''


def main():
    extract_all()

    download_json()
    keys = update_json()
    avatars = update_avatar(Path('ab/avatar.ab'))
    portraits = update_portrait(Path('ab/portraits'))
    table = Table('Update Resources',
                  headers=['Character', 'Json', 'Avatar', 'Portrait'])
    all_keys = set(keys) | set(avatars) | set(portraits)
    for key in sorted(all_keys):
        table.add_row([key, tick(key, keys), tick(key, avatars), tick(key, portraits)])
    table.print()
    with open('update.table', 'w') as f:
        table.print(f)

    clean_all()


if __name__ == '__main__':
    main()
