Author: Bhishan Poudel, Physics PhD student Ohio University
Date  : Mar 12, 2018

```
cd ~/tmp/dmstack
ls  # obs_file aliases.sh example/trial00.fits example/read_src_fits.py
rm -rf output

dstop # docker stop lsst && docker rm lsst
drun # docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0
docker exec -it lsst bash
cd /home/lsst/mnt/

source aliases.sh
cat aliases.sh
load # source /opt/lsst/software/stack/loadLSST.bash
distrib # setup lsst_distrib
obs # cd obs_file && setup -k -r . && scons && cd -

process # processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output

#dwnsrc # curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/read_src_fits.py -L -o read_src_fits.py
src # python read_src_fits.py && head src_fits.csv
```
