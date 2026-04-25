from PIL import Image
from pathlib import Path

root = Path('.')

BLANK_PNG = (255, 255, 255, 255)

BLANK_JPG = (255, 255, 255)


def blank(pixel):
    return all(el == 255 for el in pixel)


def blank_line(im, line):
    return all(blank(im.getpixel((i, line))) for i in range(im.size[0]))


def blank_col(im, col):
    return all(blank(im.getpixel((col, i))) for i in range(im.size[1]))


def first(im):
    line = 0
    while line < im.size[1] and blank_line(im, line):
        line += 1
    return line


def last(im):
    line = im.size[1] - 1
    while line >= 0 and blank_line(im, line):
        line -= 1
    return line


def left(im):
    col = 0
    while col < im.size[0] and blank_col(im, col):
        col += 1
    return col


def right(im):
    col = im.size[0] - 1
    while col >= 0 and blank_col(im, col):
        col -= 1
    return col


def getbbox(im):
    return (max(0, left(im) - 1), max(0, first(im) - 1), right(im) + 1, last(im) + 1)


def process(path, dest: Path):
    with Image.open(path) as im:
        print(path.name, end=' ')
        print(im.getbbox(), end=' ')
        box = getbbox(im)
        print(box)
        # if path.name.startswith('term3b') or 'stl' in path.name:
        #     box = (136, 21, 503, 459)
        newname = dest.joinpath(path.name)
        im = im.crop(box)
        im.save(newname)

def _trim(pict: Image.Image)->Image.Image:
        return pict.crop(getbbox(pict))
        
def trim(pict: Image.Image|str|Path)->Image:
    if not isinstance(pict, Image.Image):
        with Image.open(pict) as im:
            return _trim(im)
    else:
        return _trim(pict)

        
#work = root.joinpath('pictures')
#dest = root.joinpath('results')

#for el in work.iterdir():
#    process(el, dest)
#    print(el.name)

