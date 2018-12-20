#!python
# -*- coding: utf-8 -*-#
"""
Create sim.hdf5 and sim.txt file using src.fits.

src.fits is a fitstable obtained from obs_file package.
Clusters module needs sim.hdf5 and sim.txt so, we need to create them.

Author : Bhishan Poudel
Date   : Dec 20, 2018

Dependencies: h5py, numpy, astropy
"""
import numpy as np
import glob

from astropy.io import fits
from astropy.table import Table

# read fitstable
fitstable_path = glob.glob('output/src/*/*/src.fits')[0]
print('Reading: {}'.format(fitstable_path))

# astropy table
t = Table.read(fitstable_path,format='fits')

# RA and DEC pixels
ra_pix = t['base_NaiveCentroid_x']
dec_pix = t['base_NaiveCentroid_y']

# RA and Dec values
ra = np.abs(ra_pix*0.2/3600.-0.2) # assumes a 0.2 arcmin pixel size
dec = dec_pix*0.2/3600.

# ellipticities
e1 = t['ext_shapeHSM_HsmShapeRegauss_e1']
e2 = t['ext_shapeHSM_HsmShapeRegauss_e2']

# object id
obj_id = t['id']

# Write pipeline-compatible hdf5 file
hdf5 = 'sim.hdf5'
names = ('id', 'coord_ra_deg', 'coord_dec_deg', 'ext_shapeHSM_HsmShapeRegauss_e1', 'ext_shapeHSM_HsmShapeRegauss_e2')

t2 = Table([obj_id, ra, dec, e1, e2], names=names)

print('Writing: {}'.format(hdf5))
t2.write(hdf5, path='deepCoadd_meas', overwrite=True, format='hdf5')

# Write sim.txt file
zsim = np.zeros(len(ra))+1.5
data = np.array([obj_id, zsim])

print('Writing: sim.txt')
np.savetxt('sim.txt', data.T, fmt=['%i','%f'])
