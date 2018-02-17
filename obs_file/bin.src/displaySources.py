#!/usr/bin/env python

import argparse

import lsst.daf.persistence as dafPersist
import lsst.afw.display as afwDisplay


def do_display(repo, filename, image_dataset='calex', cat_dataset='src'):
    display = afwDisplay.getDisplay()

    butler = dafPersist.Butler(repo)
    dataId = {'filename': filename}
    exp = butler.get(image_dataset, dataId=dataId)
    src = butler.get(cat_dataset, dataId=dataId)

    with display.Buffering():
        display.mtv(exp)

        for s in src:
            if s['parent'] == 0:
                display.dot('o', s.getX(), s.getY(), ctype='blue')
            else:
                display.dot('+', s.getX(), s.getY(), ctype='red')


if __name__ == "__main__":
    description = 'Display a (calexp) image with sources' 
    epilog = 'displaySources.py /global/cscratch1/sd/wmwv/tmp/test_dr2 PTF13dad_A_J_20131020.lsst.fits --image_dataset raw --cat_dataset icSrc'
    parser = argparse.ArgumentParser(
                description=description,
                epilog=epilog,
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('repository', type=str, help='Path to output data repository')
    parser.add_argument('filename', type=str, help='Name of file that was processed')
    parser.add_argument('--image_dataset', type=str, default='calexp',
        help='Dataset to load for the image.  ["calexp", "raw"]')
    parser.add_argument('--cat_dataset', type=str, default='src',
        help='Dataset to load for the catalog.  ["src", "icSrc"]')
    args = parser.parse_args()
    do_display(args.repository, args.filename,
               image_dataset=args.image_dataset,
               cat_dataset=args.cat_dataset)
