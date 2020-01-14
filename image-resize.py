#!/usr/bin/env python

import sys


def resize(args):
    from PIL import Image

    try:    # 画像ファイルを読み込む
        im = Image.open(args.imagefile)
    except IOError:
        print('Error: image file not found.', file=sys.stderr)
        return 1

    try:
        oriantation = get_exif(im)['Orientation']
    except KeyError:
        oriantation = 1

    org_width, org_height = im.size
    res_width, res_height = (0, 0)

    if args.width and args.width > 0:
        if args.width == org_width:
            resize = False
        elif args.up:
            resize = True
        elif args.width < org_width:
            resize = True
        else:
            print(
                f'Error: image width is less than {args.width} pixels.',
                file=sys.stderr)
            return 1
        if resize:
            res_width = args.width
            res_height = (int)(org_height * args.width / org_width)

    elif args.height and args.height > 0:
        if args.height == org_height:
            resize = False
        elif args.up:
            resize = True
        elif args.height < org_height:
            resize = True
        else:
            resize = False
            print(
                f'Error: image height is less than {args.height} pixels.',
                file=sys.stderr)
            return 1
        if resize:
            res_width = (int)(org_width * args.height / org_height)
            res_height = args.height

    else:
        print(f'Error: [width | height] shuld be > 0', file=sys.stderr)
        return 1

    if resize:
        res_im = im.resize((res_width, res_height))
        if oriantation > 1:
            trans = (0, 0, 0, 3, 1, 5, 4, 6, 2)
            res_im = res_im.transpose(trans[oriantation])
        res_im.save(args.imagefile)

    return 0


def get_exif(im):
    from PIL.ExifTags import TAGS

    exif = im._getexif()
    exif_table = {}
    if exif:
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            exif_table[tag] = value

    return exif_table


if __name__ == '__main__':
    import argparse as ap

    parser = ap.ArgumentParser(
        prog='image-resize', description='Resize image file.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--width', '-w', metavar='pix',
                       type=int, help='witdh(pixel)')
    group.add_argument('--height', '-H', metavar='pix',
                       type=int, help='height(pixel)')
    parser.add_argument('--up', '-u', action='store_true',
                        help='accept scale up')
    parser.add_argument('imagefile', type=str, help='image file name')
    args = parser.parse_args()

    res = resize(args)
    sys.exit(res)
