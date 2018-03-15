Author: Bhishan Poudel, Physics PhD student Ohio University
Date  : Mar 12, 2018

```
# cd to working directory
cd ~/tmp/dmstack
ls  # obs_file aliases.sh example/trial00.fits example/read_src_fits.py

# Docker commands
dstop # docker stop lsst && docker rm lsst
drun # docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0
docker exec -it lsst bash
cd /home/lsst/mnt/

# Setup alias and load dmstack
source aliases.sh
cat aliases.sh
load # source /opt/lsst/software/stack/loadLSST.bash
distrib # setup lsst_distrib
obs # cd obs_file && setup -k -r . && scons && cd -

# Cd to example and run processCCD
cd example
rm -rf input output
mkdir input output
map # echo "lsst.obs.file.FileMapper" > input/_mapper
ingest # ingestImages.py input/ trial00.fits --mode link
crprocess # echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py
process # processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output

#dwnsrc # curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/read_src_fits.py -L -o read_src_fits.py
src # python read_src_fits.py && head src_fits.csv
```
