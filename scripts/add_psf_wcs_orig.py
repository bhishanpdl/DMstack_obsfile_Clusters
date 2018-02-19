#!/Users/poudel/Library/Enthought/Canopy/edm/envs/User/bin/python
# -*- coding: utf-8 -*-#
"""
Add given psf to random places of a cluster.

@author: Bhishan Poudel

@date: Feb 14, 2018

"""
# Imports
import os, sys
import numpy as np
import random
from astropy import wcs
from astropy.io import fits
from astropy.io.fits import getheader

def add_psf_to_cluster(EXPTIME,n_psf,psf,cluster,o_cluster):
  
  # Read psf
  psf_hdu = fits.open(psf)

  # Read cluster
  cluster_hdu = fits.open(cluster)
  cluster_hdu[0].data = cluster_hdu[0].data/EXPTIME

  # shape
  # NOTE: NAXIS = 2 means data has two axes
  NAXIS1p = getheader(psf)['NAXIS1']
  NAXIS1c = getheader(cluster)['NAXIS1']  
  # print("NAXIS1p = {}".format(NAXIS1p))
  # print("NAXIS1c = {}".format(NAXIS1c))

  # Assert fitsfiles are square shaped
  assert NAXIS1p == psf_hdu[0].data.shape[0] == psf_hdu[0].data.shape[1]
  assert NAXIS1c == cluster_hdu[0].data.shape[0] == cluster_hdu[0].data.shape[1]


  # Randomly put psf inside the cluster
  for i in range(0,n_psf):
      x = random.randint(NAXIS1p,NAXIS1c-NAXIS1p)
      y = random.randint(NAXIS1p,NAXIS1c-NAXIS1p)
      cluster_hdu[0].data[y:y+NAXIS1p, x:x+NAXIS1p] += psf_hdu[0].data

  # Get fake wcs from astropy
  w = wcs.WCS(naxis=2)
  w.wcs.crpix = [1800.0, 1800.0]
  w.wcs.crval = [0.1, 0.1]
  w.wcs.cdelt = np.array([-5.55555555555556E-05,5.55555555555556E-05])
  w.wcs.ctype = ["RA---TAN", "DEC--TAN"]
  wcs_hdr = w.to_header()
  
  # Add fake wcs to header of output file
  hdr = cluster_hdu[0].header
  hdr += wcs_hdr
  
  # Add exptime
  hdr['EXPTIME'] = EXPTIME
  cluster_hdu[0].header = hdr

  # Write output file
  cluster_hdu.writeto(o_cluster,clobber=True)
  cluster_hdu.close()
  psf_hdu.close()
  
  # Print
  print('{} PSFs added to the galaxy cluster: {}'.format(n_psf,o_cluster))

def main():
    """Run main function."""
    
    # variables
    EXPTIME = 6000.0
    n_psf = 200

    # psf and cluster
    psf = '../psf/psf_LSST20000.fits'
    psf = '../../psfb.fits'
    cluster = '../data/lsst_z0.7_0.fits'
    o_cluster = '../edited_data/wcs_psf_' + os.path.basename(cluster)
    
    add_psf_to_cluster(EXPTIME,n_psf,psf,cluster,o_cluster)   

if __name__ == "__main__":
    main()
