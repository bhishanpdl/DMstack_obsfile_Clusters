#============================ dmstack installation =============================
# install dmstack13 using conda: https://pipelines.lsst.io/v/13-0/install/conda.html
#
# 1)  conda update -n base conda
# 2) conda config --add channels http://conda.lsst.codes/stack/0.13.0
# 3) conda create --name lsst python=2
# 4) source activate lsst
# 5) conda install lsst-distrib
# 6) source eups-setups.sh
# 7) setup lsst_distrib
##==============================================================================
#
# Now we can use lsst environment
alias sbdm='source bash_dmstack.sh'
alias lsst='source activate lsst && source eups-setups.sh && setup lsst_distrib'
alias obs='cd ~/Softwares/obs_file && setup -k -r . && scons && cd -'
alias rmio='rm -rf input output'
alias map='mkdir -p input && echo "lsst.obs.file.FileMapper" > input/_mapper' # creates mapper
alias ingest='ingestImages.py input/ trial00.fits --mode link'  # input: registry.sqlite3 and raw/trial00.fits
alias crccd='echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py'
alias prccd='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'
alias src='python read_src_fits.py && head src_fits.csv'
#
#
#========================== Clusters installation ==============================
#
# NEVER install XQuartz, it caused me problems
# First install gfortran from official site
# Then install Atom, it will install Xcode, which is vital to Clusters
# Go to Aug 4, 2017 version of Clusters on github and download it to: ~/Softwares/
# cd ~/Softwares/Clusters
# pip install -r requirements.txt # pymc needs gfortran and gfortran needs Xcode, install xcode from atom.
# cd ../
# pip install Clusters/
#===============================================================================
#
# 0) python yaml_create.py # create sim.yaml
# 1) python clusters_hdf5_simtxt.py # Create sim.txt and sim.hdf5
# 2) clusters_zphot.py sim.yaml sim.hdf5  # Adding zphot_ref  to sim.hdf5
# 3) clusters_mass.py sim.yaml sim.hdf5
#
alias yml='python yaml_create.py'
alias h5='python clusters_hdf5_simtxt.py'
alias zphot='clusters_zphot.py sim.yaml sim.hdf5' # Add zphot_ref  to sim.hdf5
alias mass='clusters_mass.py sim.yaml sim.hdf5'
