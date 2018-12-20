Table of Contents
=================
   * [Using obs_file with DMstack16.0 with miniconda3](#using-obs_file-with-dmstack160-with-miniconda3)
      * [Install lsst pipelines](#install-lsst-pipelines)
      * [Go the directory having fitsfile with WCS and Stars](#go-the-directory-having-fitsfile-with-wcs-and-stars)
      * [Setup lsst environment](#setup-lsst-environment)
      * [Activate obs_file](#activate-obs_file)
      * [Create a mapper](#create-a-mapper)
      * [Ingest the fitsfile](#ingest-the-fitsfile)
      * [Process the CCD](#process-the-ccd)
      * [Final output](#final-output)
   * [Running Clusters moduel after obs_file](#running-clusters-moduel-after-obs_file)
      * [Install gfortran and XQuartz before installing Cluster](#install-gfortran-and-xquartz-before-installing-cluster)
      * [Download Cluster Package and install it (We need to install only once)](#download-cluster-package-and-install-it-we-need-to-install-only-once)
      * [Go to example directory having obs_file outputs](#go-to-example-directory-having-obs_file-outputs)
      * [Create sim.yaml and edit the path](#create-simyaml-and-edit-the-path)
      * [Create a hdf5 and a text file requried by Cluster.](#create-a-hdf5-and-a-text-file-requried-by-cluster)
      * [Now run the Cluster module](#now-run-the-cluster-module)
   * [Using obs_file with DMstack13.0 using Docker](#using-obs_file-with-dmstack130-using-docker)
      * [1.0 If you are inside docker env stop and remove lsst environment from docker](#10-if-you-are-inside-docker-env-stop-and-remove-lsst-environment-from-docker)
      * [1.1 Prepare data to use with obs_file](#11-prepare-data-to-use-with-obs_file)
      * [1.2 Setup lsst environment inside docker](#12-setup-lsst-environment-inside-docker)
      * [1.3 Setup obs_file environment](#13-setup-obs_file-environment)
      * [1.4 Ingest and process the data](#14-ingest-and-process-the-data)
      * [1.5 Look at Output](#15-look-at-output)
      * [1.6 Exit from docker](#16-exit-from-docker)
   * [Using obs_file with DMstack13.0 with miniconda2](#using-obs_file-with-dmstack130-with-miniconda2)
      * [2.1 If dmstack is not installed using miniconda2 follow the <a href="https://pipelines.lsst.io/v/13-0/install/conda.html" rel="nofollow">instructions</a>.](#21-if-dmstack-is-not-installed-using-miniconda2-follow-the-instructions)
      * [2.2 Check Miniconda environment](#22-check-miniconda-environment)
      * [2.3 Setup lsst environment](#23-setup-lsst-environment)
      * [2.4 Setup obs_file](#24-setup-obs_file)
      * [2.5 Create input and output dirs](#25-create-input-and-output-dirs)
      * [2.6 Provide the mapper](#26-provide-the-mapper)
      * [2.7 Ingest the data](#27-ingest-the-data)
      * [2.8 Process the data](#28-process-the-data)
      * [2.9 Look at the output file (src.fits)](#29-look-at-the-output-file-srcfits)
      * [Footnote:](#footnote)
 
  
Using obs_file with DMstack16.0 with miniconda3
=================================================

## Install lsst pipelines
- Follow the steps of pipelines.lsst.io and intall dmstack.
- Say yes when lsst pipeline asks to install miniconda3
- Download obs_file repo https://github.com/SimonKrughoff/obs_file/tree/tickets/DM-6924
- Place it like `~/Softwares/obs_file-tickets-DM-6924`

## Go the directory having fitsfile with WCS and Stars
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


Running Clusters moduel after obs_file
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
inside `Clsuters` each time, if we install Clusters one time we can use the module from anywhere within lsst environment.

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
## Create a hdf5 and a text file requried by `Cluster`.

We can download the script from Bhishan's git page.   
```bash
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py -L -o clusters_hdf5_simtxt.py

# NOTE:
# File website: https://github.com/bhishanpdl/DMstack_obsfile_example/blob/master/run_clusters/clusters_hdf5_simtxt.py
# Curl website: https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/run_clusters/clusters_hdf5_simtxt.py
```

## Now run the Cluster module
The steps are following:
```bash
python clusters_hdf5_simtxt.py # filenames are hard coded inside this, creates sim.txt and sim.hdf5
clusters_zphot.py sim.yaml sim.hdf5 # This will add photo-z variables in sim.hdf5
clusters_mass.py sim.yaml sim.hdf5  # This will create 3 pkl files, one log, and one main text file will mass estimate.
```
Final outputs are 3 pkl files, one log file and ONE mass estimate text file. We are interested in the Max Likelihood 
mass estimte of the cluster.
The outputs are following:
- sim_masslin_calFalse_zphot_ref.hdf5.chain.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.log
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.pkl
- sim_masslin_calFalse_zphot_ref.hdf5.m200.mass.summary.txt



Using obs_file with DMstack13.0 using Docker
==============================================

## 1.0 If you are inside docker env stop and remove lsst environment from docker
```
exit # inside the docker environment
docker stop lsst; docker rm lsst  
# docker rm $(docker ps -a -q)  # WARNING: removes all docker containers
```

## 1.1 Prepare data to use with obs_file
```
# The file trial00_good.fits is obtained from jedisim cluster simulation.
# After we get output from jedisim, we add psf and fake wcs to this and call it trial00_good.fits.
# This command is run in local computer, not inside docker.
mkdir -p ~/Temp/dmstack/example; cd ~/Temp/dmstack/example; pwd
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/trial00_good_fits.zip -L -o a.zip
unzip a.zip; mv trial00_good.fits trial00.fits; rm a.zip; rm -rf __MACOSX; clear; ls; cd ..; ls

# Now we are at `~/Temp/dmstack` directory and we have `examples` directory here.
```

## 1.2 Setup lsst environment inside docker
For the reference follow [LSST Pipelines instructions] (https://pipelines.lsst.io/install/docker.html).

```
# Before running docker open XQuartz App from Search Button
# Latest dmstack is version 16 (July 2018)
# docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v16_0
docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0 #Compatible with obs_file
docker exec -it lsst bash
cd /home/lsst/mnt/
# If we already have aliases.sh now we can do source aliases.sh
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
```

Note: We can download aliases.sh using these commands:
```
cmd t # to open new tab on terminal
cd  ~/Temp/dmstack
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/aliases.sh -L -o aliases.sh
cat aliases.sh

# now go to lsst env inside docker
source aliases.sh
```

To use these aliase we need to source this file ```source aliases.sh```.

## 1.3 Setup obs_file environment
```
# We are at ~/Temp/dmstack  directory and we have example/trail00.fits path here.
git clone https://github.com/SimonKrughoff/obs_file
cd obs_file
git checkout 21fd0d51806c43bf335300a0bc97e409ed9c703e
setup -k -r .
scons
cd ..
```

## 1.4 Ingest and process the data
```
cd example
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
ls # it should have trial00.fits and processCcdConfig.py

mkdir -p input; echo "lsst.obs.file.FileMapper" > input/_mapper

ingestImages.py input/ trial00.fits --mode link  # creates input/raw/trial00.fits  and input/registry.sqlite3

processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output
# Main output of processCcd.py is output/src/trial00/src.fits Table, ds9 can't open this talbe but fv-viewer can open this.
# We can also save the table as ascii file using the script below. (we can also save ascii from fv-viewer).
```

## 1.5 Look at Output
The output file produced is `output/src/trial00/src.fits`.
We can view this file using fv viewer. For simplicity we can set `.fit` as a 
default file extension for fv-viewer and copy src.fits to src.fit and open with
fv-viewer.
```
# Open new tab window outside of docker environment
cd ~/Temp/dmstack/example; ls
/Applications/fv.app/Contents/MacOS/fv output/src/trial00/src.fits
 ```
 
 We can also get some the important quantities from src.fits table using the 
 script `read_src_fits.py`.
 
 ```
 # Note: Generally curl downloads webpages from a link, we should use the curl command wisely (like used below ) 
 #       to download python scripts.
 curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/read_src_fits.py -L -o read_src_fits.py
 python read_src_fits.py
 head src_fits.csv
 ```
## 1.6 Exit from docker
If we want to exit from docker we may run following commands:
```
exit # inside the docker environment
docker stop lsst  
docker rm lsst  
docker rm $(docker ps -a -q)  # WARNING: removes all docker containers
```

Using obs_file with DMstack13.0 with miniconda2
================================================
## 2.1 If dmstack is not installed using miniconda2 follow the [instructions](https://pipelines.lsst.io/v/13-0/install/conda.html).

## 2.2 Check Miniconda environment
`python --version` # if it is not miniconda2 python2.7 change to that environment

## 2.3 Setup lsst environment
```bash
source activate lsst && source eups-setups.sh && setup lsst_distrib
```

## 2.4 Setup obs_file
```bash
# First download the obs_file to the folder ~/Softwares/
cd ~/Softwares/obs_file && setup -k -r . && scons && cd - && ls
```

## 2.5 Create input and output dirs
```
rm -rf input output; mkdir input output
```

## 2.6 Provide the mapper
```
mkdir input; echo "lsst.obs.file.FileMapper" > input/_mapper
```

## 2.7 Ingest the data
```
# NOTE: ingest needs  `pip install file` with ananonda2 pip., file needs libmagic.h and libmagic.dylib file.
ingestImages.py input/ trial00.fits --mode link
```

## 2.8 Process the data
```
# processCcd.py --help
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --output output --configfile processCcdConfig.py --clobber-config
```

## 2.9 Look at the output file (src.fits)
```
cp output/src/*/src.fits src.fit
/Users/poudel/Applications/fv/fv.app/Contents/MacOS/fv src.fit
```


## Footnote:
1. The obs_file was originally obtained from [Simon Krughoff](https://github.com/SimonKrughoff/obs_file/tree/tickets/DM-6924)
repository. For some reason I was getting error when I use
this repo in docker dmstack13.0 version. 
I have uploaded working version of obs_file in this github repo.

2. Another example of running obs_file can be found at github repo of [Binyang Liu](https://github.com/rbliu/Memo-Linux/blob/master/how_to_run_obs_file.md).
