"""Скрипт, що готує демонстрацію роботи з csv-файлами.

Самі приклади знаходяться в jupyter notebook."""
from pathlib import Path
import shutil
import time

SAMPLES = 'tmp'
WORK = '.'
work: Path = Path(WORK).resolve()
samples: Path = work.joinpath(SAMPLES)
BAD_CSV_SAMPLE = samples.joinpath('3_bad.csv')
SCV_SAMPLES = [samples.joinpath(f'{i}.csv') for i in range(4)]
CSV_HEADERS = samples.joinpath('h.scv')
CSV_WITH_TEXT_FIELDS = samples.joinpath('x.scv')


def printfile(path):
    with open(path, encoding='utf-8') as f:
        while s := f.read(64):
            print(s, end='')
    print()


def write_str(dest, source, encoding=None):
    with open(dest, 'w', encoding=encoding) as f:
        f.write(source)


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


def _prepare_csv():
    write_str(SCV_SAMPLES[0],
              'field 1, field 2, field3\n1,1,int\n2,4,int\n1.5, 2.25, float')
    write_str(SCV_SAMPLES[1],
              'field 1, field 2, field3\n1, 345 , qwerty   \n2,,1.45\nasd,,')
    write_str(SCV_SAMPLES[2],
              'field 1, field 2, field3\n1,1,int,\n2,4,int,smth\n1.5, 2.25, float')
    write_str(BAD_CSV_SAMPLE,
              'field 1, field 2, field3\n1,1,int,\n2,4,"int,smth\n1.5, 2.25, float')


def prepare_3():
    try:
        del_folder(samples)
        samples.mkdir()
        _prepare_csv()
        return True
    except BaseException as e:
        print(e)
        return False
