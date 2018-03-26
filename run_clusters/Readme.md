# Using Cluster module to estimate the mass of the cluster

## Install Clusters
First go to the [Clusters link](https://github.com/nicolaschotard/Clusters) then go to commits and download the directory `Clusters` from the date  Aug 4,2017 and make it `~/Softwares/Clusters`.

Then we must activate lsst enivronment.
```
source activate lsst
source eups-setups.sh
setup lsst_distrib
```

Now cd to the `Clusters` directory and install the module.
Note that we must install `XQuartz` and `gfortan` before installing `Clusters`.
Especially the `pymc` module needs fortran compiler `gfortran` for the installation.
Go to [official link](https://gcc.gnu.org/wiki/GFortranBinaries#MacOS) to download `gofrtran`, unpack the `.pkg` file and right click and open it to install.
```
NEVER install XQuartz, it caused me problems
First install gfortran from official site
Then install Atom, it will install Xcode, which is vital to Clusters
Go to Aug 4, 2017 version of Clusters on github and download it to: ~/Softwares/
cd ~/Softwares/Clusters
pip install -r requirements.txt # pymc needs gfortran and gfortran needs Xcode, install xcode from atom.
cd ../
pip install Clusters/
```

## After installing `Clusters` cd to example directory
```
cd /Users/poudel/Temp/dmstack/example
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/sim.yaml -L -o sim.yaml
```


The file `sim.yaml` looks like this:  
```
{
    "cluster": "SIM_cluster",
    "ra": 0.1,
    "dec": 0.1,
    "redshift": 0.3,
    "filter": ["u", "g", "r", "i", "i2", "z"],
    "butler": "/Users/poudel/Temp/dmstack/example/output",
    "keys": {'src':["id", "coord*", "ext_shapeHSM_HsmSourceMoments_x", "ext_shapeHSM_HsmSourceMoments_y", "ext_shapeHSM_HsmShapeRegauss_e1", "ext_shapeHSM_HsmShapeRegauss_e2"]},
    "sim": {"flag" : True, "zfile":"sim.txt"},
    "mass":{ "zconfig" : "zphot_ref",
             "mprior":'lin'}
}
```

## Create a hdf5 and a text file requried by `Cluster`.

We can download the script from Bhishan's git page.   
```
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py -L -o clusters_hdf5_simtxt.py

# NOTE:
# File website: https://github.com/bhishanpdl/DMstack_obsfile_example/blob/master/run_clusters/clusters_hdf5_simtxt.py
# Curl website: https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py
```

## Now run the Cluster module
The steps are following:
```
1) python clusters_hdf5_simtxt.py # filenames are hard coded inside this, creates sim.txt and sim.hdf5
2) clusters_zphot.py sim.yaml sim.hdf5 # This will add photo-z variables in sim.hdf5
3) clusters_mass.py sim.yaml sim.hdf5  # This will create 3 pkl files, one log, and one main text file will mass estimate.
```
Final outputs are 3 pkl files, one log file and ONE mass estimate text file. We are interested in the Max Likelihood 
mass estimte of the cluster.

- sim_masslin_calFalse_zphot_ref.hdf5.chain.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.log
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt

