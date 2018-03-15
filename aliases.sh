
# Bhishan's shortcuts
alias c='clear'
alias cls='clear; ls'
alias ..='cd ..'

# Setup DM stack
alias load='source /opt/lsst/software/stack/loadLSST.bash'
alias distrib='setup lsst_distrib'
alias obs='cd obs_file && setup -k -r . && scons && cd ..'
alias catal='cat /home/lsst/mnt/aliases.sh'

# now cd to example and mkdir input; rm -rf output
alias map='echo "lsst.obs.file.FileMapper" > input/_mapper'
alias ingest='ingestImages.py input/ trial00.fits --mode link'
alias crprocess='echo "config.charImage.repair.cosmicray.nCrPixelMax=1000000" > processCcdConfig.py'
alias process='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'

alias dwnsrc='curl https://github.com/bhishanpdl/DMstack_obsfile_example/raw/master/example/read_src_fits.py -L -o read_src_fits.py'
alias src='python read_src_fits.py && head src_fits.csv'

# cmt t (go to next tab), then open src.fits using fv-viewer app
alias out='/Applications/fv/fv.app/Contents/MacOS/fv output/src/trial00/src.fits'

