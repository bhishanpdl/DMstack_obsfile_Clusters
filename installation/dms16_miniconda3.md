Using obs_file with DMstack16.0 with miniconda3
=================================================

## Install lsst pipelines
- Follow the steps of [pipelines.lsst.io](https://pipelines.lsst.io/) and install dmstack.
- Say yes when lsst pipeline asks to install miniconda3
- Download obs_file repo https://github.com/SimonKrughoff/obs_file/tree/tickets/DM-6924
- Place it like `~/Softwares/obs_file-tickets-DM-6924`

## Go to the directory having fitsfile with WCS and Stars
```bash
cd ~/mydmstack/example
ls # trial00.fits
```

## Setup lsst environment
```
source ~/lsst_stack/loadLSST.bash
setup lsst_distrib
```

## Activate obs_file
```
cd ~/Softwares/obs_file-tickets-DM-6924 && setup -k -r . && scons && cd -
```

## Create a mapper
```
cd ~/mydmstack/examples
rm -r input output
mkdir input output
echo "lsst.obs.file.fileMapper.FileMapper" > input/_mapper
```

## Ingest the fitsfile
```
ingestImages.py input/ trial00.fits --mode link
```

## Process the CCD
```
echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py
processCcd.py input/ --id filename=trial00.fits extname=UNKNOWN --config isr.noise=5 --output output --configfile processCcdConfig.py --clobber-config
```

## Final output
```
mydmstack/example/output/src/UNKNOWN/trial00/src.fits
output/src/UNKNOWN/trial00/src.fits # the ouput directory is created if not existent, but we need to create input dir.

# this is a fitstable not an fitsimage
# we can we fv-viewer to view this table.
```


Running Clusters module after obs_file
========================================
After we run obs_file we get the fitstable called `src.fits` having copious number of columns.
To get the mass estimation using RA, DEC, and ellipticities we use [Clusters](https://github.com/nicolaschotard/Clusters) module.

## Install gfortran and XQuartz before installing Cluster
- Install from [official link](https://gcc.gnu.org/wiki/GFortranBinaries#MacOS).
- Install XQartz from App Store. (It did not worked for dm13.0 but worked for dm16.0)

## Download Cluster Package and install it (We need to install only once)
- Download the repo [Clusters](https://github.com/nicolaschotard/Clusters) and place it like `~/Softwares/Clusters`.
```bash
cd ~/Softwares/Clusters
pip install -r requirements.txt # pymc needs gfortran and gfortran needs Xcode, install xcode from app store.
cd ../
pip install Clusters/
```

## Go to example directory having obs_file outputs
Unlike obs_file moudule where we need to go each time and run `setup -k -r . && scons` we do not need to go
inside `Clusters` each time, if we install Clusters one time we can use the module from anywhere within lsst environment.

## Create sim.yaml and edit the path
```bash
cd /Users/poudel/Temp/dmstack/example
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/sim.yaml -L -o sim.yaml
```

```yaml
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
## Create sim.hdf5 and sim.txt required by `Cluster`.

We can download the script from github
```bash
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py -L -o clusters_hdf5_simtxt.py

# NOTE:
# File website: https://github.com/bhishanpdl/DMstack_obsfile_example/blob/master/run_clusters/clusters_hdf5_simtxt.py
# Curl website: https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py
```

## Run the Cluster module
The steps are following:
```bash
# step1: creates sim.txt and sim.hdf5
# filenames are hard coded inside the code.
python clusters_hdf5_simtxt.py

# step2: add photo-z variables to the file sim.hdf5
clusters_zphot.py sim.yaml sim.hdf5

# step3: Run the main program to estimate mass
# This will create 3 pkl files, one log, and one main text file will mass estimate.
# This will take about 15 minutes to finish. Will run about 10k iterations.
clusters_mass.py sim.yaml sim.hdf5

```
Final outputs are 3 pkl files, one log file and ONE mass estimate text file. We are interested in the Max Likelihood mass estimte of the cluster.
The outputs are following:
- sim_masslin_calFalse_zphot_ref.hdf5.chain.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.log
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt

Exmaple:
```
# File: sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt
mean	6.947353e+14
stddev	2.675523e+14
Q2.5	2.309040e+14
Q25	4.899290e+14
Q50	6.687590e+14
Q75	8.893375e+14
Q97.5	1.208473e+15
HPD68	3.238060e+14	8.775934e+14
HPD95	2.259573e+14	1.195459e+15
MaxLike	4.936213e+14	1.670360e+14	3.870734e+14
Log10 Maxlike	1.473170e+01	6.239960e-02	2.875080e-01


Meaning:
Estimated mass of cluster = 4.936 solar mass
```