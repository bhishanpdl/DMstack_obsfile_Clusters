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
mkdir ~/tmp/dmstack/example; cd ~/tmp/dmstack/example; pwd
curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/trial00_good_fits.zip -L -o a.zip
unzip a.zip; mv trial00_good.fits trial00.fits
```

## 2. Setup lsst environment inside docker
```
docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0
docker exec -it lsst bash
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
cd /home/lsst/mnt/
```

## 3. Setup obs_file environment
```
mkdir -p  ~/tmp/dmstack
cd ~/tmp/dmstack
git clone https://github.com/SimonKrughoff/obs_file
cd obs_file
git checkout 21fd0d51806c43bf335300a0bc97e409ed9c703e
setup -k -r .
scons
cd ..
```

## 4. Ingest and process the data
```
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
ls # it should have trial00.fits and processCcdConfig.py
mkdir input output

echo "lsst.obs.file.FileMapper" > input/_mapper

ingestImages.py input/ trial00.fits --mode link

processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output
```

## 5. Exit from docker
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
