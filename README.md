# Example of running obs_file in Docker
This repo is a basic tutorial how to get started with using DMstack and obs_file
in Docker.

## Setup lsst environment inside docker
```
docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0
docker exec -it lsst bash
source /opt/lsst/software/stack/loadLSST.bash
setup lsst_distrib
cd /home/lsst/mnt/
```

## Setup obs_file environment
```
cd /path/to/DMstack_obsfile_example
cd obs_file
setup -k -r .
scons
cd ..
```

# Ingest and process the data
```
cd example
ls # it should have trail0.fits and processCcdConfig.py
mkdir input output

echo "lsst.obs.file.FileMapper" > input/_mapper

ingestImages.py input/ trial0.fits --mode link

processCcd.py input/ --id filename=trial0.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output
```

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
