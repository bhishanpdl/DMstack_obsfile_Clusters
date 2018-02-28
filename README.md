# Example of running obs_file in Docker (using DMstack13.0)
This repo is a basic tutorial how to get started with using DMstack and obs_file
in Docker.

## 0. Stop and Remove lsst environment from docker
```
exit # inside the docker environment
docker stop lsst; docker rm lsst  
# docker rm $(docker ps -a -q)  # WARNING: removes all docker containers
```

## 1. Prepare data to use with obs_file
```
# The file trial00_good.fits is obtained from jedisim cluster simulation.
# After we get output from jedisim, we add psf and fake wcs to this and call it trial00_good.fits.
mkdir ~/tmp/dmstack/example; cd ~/tmp/dmstack/example; pwd
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/trial00_good_fits.zip -L -o a.zip
unzip a.zip; mv trial00_good.fits trial00.fits; rm a.zip; rm -rf __MACOSX; clear; ls; cd ..
```

## 2. Setup lsst environment inside docker
```
# Before running docker open XQuartz App from Search Button
docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0
docker exec -it lsst bash
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
cd /home/lsst/mnt/
```

**Optional**
After mounting to local drive we can use some of the aliases.
```bash
# File: ~/tmp/dmstack/aliases.sh
alias cls='clear; ls'
alias ..='cd ..'

alias obs='cd obs_file && setup -k -r . && scons && cd ..'
alias ingest='ingestImages.py input/ trial00.fits --mode link'
alias process='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'
```

To use these aliase we need to source this file ```source aliases.sh```.

## 3. Setup obs_file environment
```
# We are at ~/tmp/dmstack  directory and we have example/trail00.fits path here.
git clone https://github.com/SimonKrughoff/obs_file
cd obs_file
git checkout 21fd0d51806c43bf335300a0bc97e409ed9c703e
setup -k -r .
scons
cd ..
```

## 4. Ingest and process the data
```
cd example
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
ls # it should have trial00.fits and processCcdConfig.py
mkdir input output

echo "lsst.obs.file.FileMapper" > input/_mapper

ingestImages.py input/ trial00.fits --mode link  # creates input/raw/trial00.fits  and input/registry.sqlite3

processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output
```

## 5. Look at Output
The output file produced is `output/src/trial00/src.fits`.
We can view this file using fv viewer. For simplicity we can set `.fit` as a 
default file extension for fv-viewer and copy src.fits to src.fit and open with
fv-viewer.
```
# Open new tab window outside of docker environment
cd ~/tmp/dmstack; ls
cp output/src/trial00/src.fits output/src/trial00/src.fit
/Applications/fv/fv.app/Contents/MacOS/fv output/src/trial00/src.fit
 ```
 
 We can also get some the important quantities from src.fits table using the 
 script `read_src_fits.py`.
 
 ```
 curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/read_src_fits.py -L -o read_src_fits.py
 python read_src_fits.py
 head src_fits.csv
 ```
## 6. Exit from docker
If we want to exit from docker we may run following commands:
```
exit # inside the docker environment
docker stop lsst  
docker rm lsst  
docker rm $(docker ps -a -q)  # WARNING: removes all docker containers
```

## Footnote:
1. The obs_file was originally obtained from [Simon Krughoff](https://github.com/SimonKrughoff/obs_file/tree/tickets/DM-6924)
repository. For some reason I was getting error when I use
this repo in docker dmstack13.0 version. 
I have uploaded working version of obs_file in this github repo.

1. This example is based on a repo by [Binyang Liu] (https://github.com/rbliu/Memo-Linux/blob/master/how_to_run_obs_file.md)
