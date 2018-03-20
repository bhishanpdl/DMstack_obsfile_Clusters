# Using Cluster module to estimate the mass of the cluster

The steps are following:
```
1) python clusters_hdf5_simtxt.py # filenames are hard coded, created sim.txt and sim.hdf5
2) clusters_zphot.py sim.yaml sim.hdf5
3) clusters_mass.py sim.yaml sim.hdf5
```

Here, from the `jedisim` we get `lsst0.fits`. We add wcs and psf and call it `trial00.fits`. Then we use `processCcd.py` to get the file `/home/bhishan/Research/a2_dmstack/dmstack_example/example/output/src/trial00/src.fits`.


The file `sim.yaml` looks like this:  
```
{
    "cluster": "SIM_cluster",
    "ra": 0.1,
    "dec": 0.1,
    "redshift": 0.3,
    "filter": ["u", "g", "r", "i", "i2", "z"],
    "butler": "/home/bhishan/Research/a2_dmstack/dmstack_example/example/output",
    "keys": {'src':["id", "coord*", "ext_shapeHSM_HsmSourceMoments_x", "ext_shapeHSM_HsmSourceMoments_y", "ext_shapeHSM_HsmShapeRegauss_e1", "ext_shapeHSM_HsmShapeRegauss_e2"]},
    "sim": {"flag" : True, "zfile":"sim.txt"},
    "mass":{ "zconfig" : "zphot_ref",
             "mprior":'lin'}
}
```


The final outputs of `cluster_mass.py sim.yaml sim.hdf5` is `sim_masslin_something.txt`.
The script `cluster_mass.py` creates 5 files (one text, one log, and 3 pkl files):  
- sim_masslin_calFalse_zphot_ref.hdf5.chain.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.log
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt

