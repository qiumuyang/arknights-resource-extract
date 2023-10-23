from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile


def extract_zip(f: ZipFile,
                path_from: str,
                path_to: str,
                overwrite: bool = False,
                silent: bool = True):
    """Extract a file or directory from a zip file.

    Args:
        f: the ZipFile object.
        path_from: the path of the file or directory to extract.
        path_to: the path to extract to.
    """
    if path_from.endswith('/'):
        # extract directory
        target_dir = Path(path_to)
        if target_dir.is_file():
            raise FileExistsError(
                f'Expected an output directory, got a file: {path_to}')
        target_dir.mkdir(parents=True, exist_ok=True)

        files = []
        for name in f.namelist():
            if name.startswith(path_from):
                to = name[len(path_from):]
                if to:
                    target_file = target_dir / to
                    target_file.parent.mkdir(parents=True, exist_ok=True)
                    if target_file.exists() and not overwrite:
                        if not silent:
                            print(f'File already exists: {target_file}')
                        continue
                    target_file.write_bytes(f.read(name))
                    print(f'Extracted: {name} => {target_file}')
                    files.append(target_file)
        return files
    else:
        # extract file
        target_file = Path(path_to)
        # if target_file.is_dir():
        #     raise FileExistsError(
        #         f'Expected an output file, got a directory: {path_to}')
        # target_file.parent.mkdir(parents=True, exist_ok=True)
        # if target_file.exists() and not overwrite:
        #     if not silent:
        #         print(f'File already exists: {target_file}')
        #     return target_file
        # target_file.write_bytes(f.read(path_from))
        # print(f'Extracted: {path_from} => {target_file}')
        if target_file.exists():
            raise FileExistsError(f'File already exists: {target_file}')

        # use regex to match
        import re
        pattern = re.compile(path_from)
        matched = []
        for name in f.namelist():
            if pattern.match(name):
                matched.append(name)

        if len(matched) == 0:
            raise FileNotFoundError(f'File not found: {path_from}')
        elif len(matched) > 1 and not path_to.endswith('/'):
            raise RuntimeError(
                f'Multiple files matched: {matched}, expected a directory: {path_to}'
            )

        if not path_to.endswith('/'):
            target_file.write_bytes(f.read(matched[0]))
            print(f'Extracted: {matched[0]} => {target_file}')
            return target_file

        target_dir = target_file
        target_dir.mkdir(parents=True, exist_ok=True)
        target_files = []
        for name in matched:
            to = Path(name).name
            target_file = target_dir / to
            target_file.write_bytes(f.read(name))
            print(f'Extracted: {name} => {target_file}')
            target_files.append(target_file)
        return target_files


def extract_all(path_to_apk: str, overwrite: bool = False):
    file = ZipFile(path_to_apk)
    # Step 1: Data Table (fetch from github instead)
    # extract_zip(file, 'assets/AB/Android/gamedata/excel/character_table.ab', '../ab/character_table.ab')
    # extract_zip(file, 'assets/AB/Android/gamedata/excel/charword_table.ab', '../ab/charword_table.ab')
    # Step 2: Avatar
    extract_zip(
        file,
        r'assets/AB/Android/spritepack/ui_char_avatar_\d+.ab',
        r'ab/avatar/',
        overwrite=overwrite,
    )
    # Step 3: Portrait
    extract_zip(
        file,
        'assets/AB/Android/arts/charportraits/',
        'ab/portraits/',
        overwrite=overwrite,
    )
    # Step 4: Tachie (often incomplete, manual update required)
    extract_zip(
        file,
        'assets/AB/Android/chararts/',
        'ab/chararts/',
        overwrite=overwrite,
    )


def clean_all():
    import shutil
    shutil.rmtree('ab', ignore_errors=True)


if __name__ == '__main__':
    extract_all("base.apk")
