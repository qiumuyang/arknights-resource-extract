from pathlib import Path
from zipfile import ZipFile


def extract_zip(f: ZipFile, path_from: str, path_to: str):
    if path_from.endswith('/'):
        target_dir = Path(path_to)
        if target_dir.is_file():
            raise FileExistsError(f'path_to is a file: {path_to}')
        target_dir.mkdir(parents=True, exist_ok=True)

        files = []
        # extract directory
        for name in f.namelist():
            if name.startswith(path_from):
                to = name[len(path_from):]
                if to:
                    target_file = target_dir / to
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    target_file.write_bytes(f.read(name))
                    print(f'Extracted: {name} => {target_file}')
                    files.append(target_file)
        return files
    else:
        # extract file
        target_file = Path(path_to)
        if target_file.is_dir():
            raise FileExistsError(f'path_to is a directory: {path_to}')
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_bytes(f.read(path_from))
        print(f'Extracted: {path_from} => {target_file}')
        return target_file


def extract_all():
    file = ZipFile('base.apk')
    # Step 1: Data Table (decode method unknown, deprecated)
    # extract_zip(file, 'assets/AB/Android/gamedata/excel/character_table.ab', '../ab/character_table.ab')
    # extract_zip(file, 'assets/AB/Android/gamedata/excel/charword_table.ab', '../ab/charword_table.ab')
    # Step 2: Avatar
    extract_zip(file, 'assets/AB/Android/spritepack/ui_char_avatar_h1_0.ab', 'ab/avatar.ab')
    # Step 3: Portrait
    extract_zip(file, 'assets/AB/Android/arts/charportraits/', 'ab/portraits/')
    # Step 4: Tachie (often incomplete, manual update required)
    extract_zip(file, 'assets/AB/Android/chararts/', 'ab/chararts/')


def clean_all():
    import shutil
    shutil.rmtree('ab', ignore_errors=True)


if __name__ == '__main__':
    extract_all()
