Using obs_file with DMstack13.0 with miniconda2
================================================

## 2.1 If dmstack is not installed using miniconda2 follow the [instructions](https://pipelines.lsst.io/v/13-0/install/conda.html).

```bash
## 2.2 Check Miniconda environment
python --version # if it is not miniconda2 python2.7 change to that environment

## 2.3 Setup lsst environment

source activate lsst && source eups-setups.sh && setup lsst_distrib

## 2.4 Setup obs_file
# First download the obs_file to the folder ~/Softwares/
cd ~/Softwares/obs_file && setup -k -r . && scons && cd - && ls


## 2.5 Create input and output dirs
rm -rf input output; mkdir input output


## 2.6 Provide the mapper
mkdir input; echo "lsst.obs.file.FileMapper" > input/_mapper


## 2.7 Ingest the data
# NOTE: ingest needs  `pip install file` with ananonda2 pip., file needs libmagic.h and libmagic.dylib file.
ingestImages.py input/ trial00.fits --mode link


## 2.8 Process the data
# processCcd.py --help
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --output output --configfile processCcdConfig.py --clobber-config


## 2.9 Look at the output file (src.fits)
cp output/src/*/src.fits src.fit
/Users/poudel/Applications/fv/fv.app/Contents/MacOS/fv src.fit
```
