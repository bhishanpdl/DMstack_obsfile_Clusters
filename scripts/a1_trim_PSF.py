#!python
# -*- coding: utf-8 -*-#
"""
Trim the psf to a given size.

@author: Bhishan Poudel

@date:  Feb 19, 2018

@email: bhishanpdl@gmail.com

"""
# Imports
import numpy as np
from astropy.io import fits
import sys

def trim_psf(psf,x,y,r,scale_up):
    data = fits.getdata(psf)
    data_trim = data[y-r:y+r,x-r:x+r] * scale_up
      
        
    ofile = 'trimmed_' + psf
    print('Creating: ', ofile)
    fits.writeto(ofile,data_trim,overwrite=True)

def main():
    """Run main function."""
#    psf = 'psf/psfb.fits'
    psf = sys.argv[1]
    x = 2035 # opening psf in ds9, center was 2035,2015
    y = 2015
    r = 20
    scale_up = sys.argv[2]

    # prints
    print('Input psf: ', psf)
    print('Center of psf: ', x, ' ', y)
    print('Radius of psf: ', r)
    print('Scale up: ', scale_up)
    trim_psf(psf,x,y,r,scale_up)

if __name__ == "__main__":
    main()
