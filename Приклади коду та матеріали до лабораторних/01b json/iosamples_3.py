"""Скрипт, що готує демонстрацію роботи з json-файлами.

Самі приклади знаходяться в jupyter notebook."""
from pathlib import Path
import shutil
import time

SAMPLES = 'tmp'
WORK = '.'
work: Path = Path(WORK).resolve()
samples: Path = work.joinpath(SAMPLES)
JSON_SAMPLE = samples.joinpath('1.json')


def printfile(path):
    with open(path, encoding='utf-8') as f:
        while s := f.read(64):
            print(s, end='')
    print()


def del_folder(folder, tries=5):
    to_do = True
    exist = folder.exists()
    n = tries
    while to_do and exist:
        shutil.rmtree(folder, ignore_errors=True)
        if exist := folder.exists():
            time.sleep(0.1)
            n -= 1
            if n == 0:
                ans = input(f'Folder {folder!s} still exists. Try once more? (Y/N)').strip().lower()
                if ans[0] in {'y', 'н'}:
                    n = tries
                else:
                    to_do = False
    if exist:
        raise RuntimeError(f'Unable to remove folder {folder!s}')


def prepare_3():
    try:
        del_folder(samples)
        samples.mkdir()
        return True
    except BaseException as e:
        print(e)
        return False
