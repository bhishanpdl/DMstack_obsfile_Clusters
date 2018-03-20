# First install dmstack13 using conda: https://pipelines.lsst.io/v/13-0/install/conda.html
#
# 1)  conda update -n base conda
# 2) conda config --add channels http://conda.lsst.codes/stack/0.13.0
# 3) conda create --name lsst python=2
# 4) source activate lsst
# 5) conda install lsst-distrib
# 6) source eups-setups.sh
# 7) setup lsst_distrib
#
# Now we can use lsst environment
alias sbdm='source bash_dmstack.sh'
alias lsst='source activate lsst && source eups-setups.sh && setup lsst_distrib'
alias obs='cd ~/Softwares/obs_file && setup -k -r . && scons && cd -'

# cd example;  rm -rf input output && mkdir input output

alias map='mkdir -p input && echo "lsst.obs.file.FileMapper" > input/_mapper' # creates mapper
alias ingest='ingestImages.py input/ trial00.fits --mode link'  # input: registry.sqlite3 and raw/trial00.fits
alias crccd='echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py'
alias prccd='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'
alias src='python read_src_fits.py && head src_fits.csv'

# from obs_file we get: output/src/trial00/src.fits
#
#
# To install Cluster
# pwd: examples
# cd ../
# cd Clusters; pip install -r requirements.txt
# NOTE: Failed: pip install pymc
# PASS: conda install pymc
# cd ../
# pip install Clusters/
#
# First edit:  sim.yaml and clusters_import_simcat.py files.
#
# 1) python clusters_import_simcat.py
# 2) clusters_zphot.py sim.yaml sim.hdf5
# 3) clusters_mass.py sim.yaml sim.hdf5
