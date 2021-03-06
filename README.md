Using obs_file with DMstack13.0 with miniconda2
================================================
## 2.1 Installation of dmstack and obs_file

- If dmstack is not installed using miniconda2 follow the [instructions](https://pipelines.lsst.io/v/13-0/install/conda.html).
- Download the compatible branch of [obs_file](https://github.com/SimonKrughoff/obs_file/tree/tickets/DM-6924) and put it as `~/Softwares/obs_file-tickets-DM-6924`

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
```bash
rm -rf input output; mkdir input output
```

## 2.6 Provide the mapper
```bash
mkdir input; echo "lsst.obs.file.FileMapper" > input/_mapper
```

## 2.7 Ingest the data
```bash
# NOTE: ingest needs  `pip install file` with ananonda2 pip., file needs libmagic.h and libmagic.dylib file.
ingestImages.py input/ trial00.fits --mode link
```

## 2.8 Process the data
```bash
# processCcd.py --help
echo 'config.charImage.repair.cosmicray.nCrPixelMax=1000000' > processCcdConfig.py
processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --output output --configfile processCcdConfig.py --clobber-config
```

## 2.9 Look at the output file (src.fits)
```bash
cp output/src/*/src.fits src.fit
/Users/poudel/Applications/fv/fv.app/Contents/MacOS/fv src.fit
```

# NOTES
- We can check installed dmstack version using conda channel used. `cat ~/.condarc`.
  Currently I have been using dmstack 13 in computer simplici.
- The current version of github `obs_file` is not compatible with dmstack13, so
  I have already copied the compatible github branch of obs file here in my github repo.
- The module `Clusters` is only used for mass estimation, I need not to use this.
