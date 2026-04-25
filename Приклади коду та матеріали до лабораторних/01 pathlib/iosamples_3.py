from pathlib import Path
# import os
import shutil
import time

TEST = 'TestDir'
SAMPLES = 'Samples'
WORK = '.'
work: Path = Path(WORK).resolve()
test: Path = work.joinpath(TEST)
samples: Path = test.joinpath(SAMPLES)


def show(fname):
    print('size of ' + fname + ' is :', Path(fname).stat().st_size)
    print('content of ' + fname + ' is:')
    with open(fname, encoding='utf-8') as f:
        s = f.read()
    print(s, end='')
    print('\nof length', len(s))
    print('as repr:', repr(s), sep='\n')
    print('if read as binary:')
    with open(fname, 'rb') as f:
        s = f.read()
    print(s)


def printfile(path):
    with open(path, encoding='utf-8') as f:
        while s := f.read(64):
            print(s, end='')
    print()


def show_tree(path='.'):
    path = Path(path)
    if not path.exists():
        print(f'Path {path!s} is not exist!')
        return
    _show_tree(path, 0)


def _show_tree(path: Path, n: int):
    for p in path.iterdir():
        print('---' * n, p.name, sep='')
        if p.is_dir():
            _show_tree(p, n + 1)


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


def _prepare_dir1(sample_dir, symlink):
    sample_dir.mkdir()
    d1 = sample_dir.joinpath('1')
    d2 = sample_dir.joinpath('2')
    d1.mkdir(exist_ok=True)
    d2.mkdir(exist_ok=True)
    write_str(d1.joinpath('1.txt'), 'qwerty')
    write_str(d1.joinpath('2.txt'), 'qwerty')
    write_str(d2.joinpath('3.txt'), 'qwerty')
    if symlink:
        d1.joinpath('4.txt').symlink_to(d1.joinpath('1.txt'))


def _prepare_dir2(sample_dir):
    sample_dir.mkdir()
    d1 = sample_dir.joinpath('1')
    d2 = sample_dir.joinpath('2')
    d1.mkdir(exist_ok=True)
    d2.mkdir(exist_ok=True)
    write_str(d1.joinpath('1.txt'), 'qwerty')
    write_str(d1.joinpath('2.txt'), 'qwe1ty')
    write_str(d2.joinpath('4.txt'), 'qwerty')


def prepare_3(symlink=True):
    try:
        del_folder(test)
        test.mkdir()
        samples.mkdir()
        _prepare_dir1(test.joinpath('X'), symlink=symlink)
        _prepare_dir2(test.joinpath('Y'))
        return True
    except BaseException as e:
        print(e)
        return False


def unlink_folder(folder):
    """ Remove files from folder`s root."""
    p = Path(folder)
    for el in p.iterdir():
        if el.is_file():
            el.unlink()
