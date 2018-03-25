#!python
# -*- coding: utf-8 -*-#
"""
Reading fitsfile table

@author: Bhishan Poudel

@date: Mar 24, 2018


"""
# Imports
import numpy as np
import os
import shutil
import glob

def read_mass():
    # 'MaxLike	1.153734e+15	2.949554e+14	6.627750e+14'
    infile = 'sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt'

    with open(infile) as fi:
        for line in fi:
            # MaxLike	1.153734e+15	2.949554e+14	6.627750e+14
        	if line.lstrip().startswith('MaxLike'):
        		mass = line.split()[1]
        		print("MaxLike mass = {}".format(mass))


    with open('MaxLike_mass.txt','w') as fo:
        fo.write(mass)

    for f in glob.glob('*.pkl'):
        print('Deleting: ', f)
        os.remove(f)

    for f in glob.glob('*.log'):
        print('Deleting: ', f)
        os.remove(f)

    if not os.path.isdir('mass_summary'):
        print('Creating: ', 'mass_summary')
        os.makedirs('mass_summary')

    shutil.copyfile(infile, 'mass_summary/mass_summary1.txt')


def main():
    """Run main function."""
    read_mass()



if __name__ == "__main__":
    main()
