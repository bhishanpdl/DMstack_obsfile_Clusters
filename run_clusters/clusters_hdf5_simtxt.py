import pyfits
import astropy.table as table
import numpy as np
import sys


def create_hdf5_simtext(in_src_fits, hdf5,sim_text):
    """
    Create Clusters pipeline-compatible hdf5 from simulated files.

    input: src.fits        #  obtained from processCcd.py script of dmstack.

    outputs: a) sim.hdf5   # astropy-table compatible with Cluster pipelines
             b) sim.txt    # text file required by cluster scripts.
    """
    cat_sim = pyfits.open(in_src_fits)

    # ra and dec
    # ra = cat_sim[1].data['coord_ra']
    # dec = cat_sim[1].data['coord_dec']
    ra_pix = cat_sim[1].data['base_GaussianCentroid_X']
    dec_pix = cat_sim[1].data['base_GaussianCentroid_y']
    ra = np.abs(ra_pix*0.2/3600.-0.2) # assumes a 0.2 arcmin pixel size
    dec = dec_pix*0.2/3600.


    e1 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e1']
    e2 = cat_sim[1].data['ext_shapeHSM_HsmShapeRegauss_e2']
    obj_id = cat_sim[1].data['id']

    # Write pipeline-compatible hdf5 file
    deepCoadd_meas = table.Table([obj_id, ra, dec, e1, e2], names=('id', 'coord_ra_deg', 'coord_dec_deg', 'ext_shapeHSM_HsmShapeRegauss_e1', 'ext_shapeHSM_HsmShapeRegauss_e2'))

    # Write hdf5
    print('Creating: {}'.format(hdf5))
    deepCoadd_meas.write(hdf5, path='deepCoadd_meas', overwrite=True)

    # write the text file
    zsim = np.zeros(len(ra))+1.5
    data = np.array([obj_id, zsim])
    print('Creating: {}'.format(sim_text))
    np.savetxt(sim_text, data.T, fmt=['%i','%f'])


if __name__ == '__main__':

    in_src_fits = '/home/bhishan/Research/a2_dmstack/dmstack_example/example/output/src/trial00/src.fits'
    hdf5 = 'sim.hdf5'    # used by: clusters_mass.py and clusters_mass.py
    sim_text = 'sim.txt' # inside sim.yaml ==> "sim": {"flag" : True, "zfile":"sim.txt"}
    create_hdf5_simtext(in_src_fits, hdf5,sim_text)
