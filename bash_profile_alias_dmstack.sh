##==============================================================================
# Docker aliases
##==============================================================================
alias mydocker='docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0'
alias drun='docker run -itd --name lsst -v `pwd`:/home/lsst/mnt lsstsqre/centos:7-stack-lsst_distrib-v13_0'
alias dexec='docker exec -it lsst bash, echo "Now type cd /home/lsst/mnt/  inside the docker vagrant "'
alias dmout='/Applications/fv.app/Contents/MacOS/fv output/src/trial00/src.fits'
alias dstop='docker stop lsst && docker rm lsst'

# the syntax cat <<EOF is called a "here document".
function aliasd(){
  if [ ! -f myfile ]
then
   cat <<EOF > aliases.sh
   alias c='clear'
   alias cls='clear; ls'
   alias ..='cd ..'

   alias load='source /opt/lsst/software/stack/loadLSST.bash'
   alias distrib='setup lsst_distrib'

   alias obs='cd obs_file && setup -k -r . && scons && cd ..'
   alias ingest='ingestImages.py input/ trial00.fits --mode link'
   alias process='processCcd.py input/ --id filename=trial00.fits --config isr.noise=5 --configfile processCcdConfig.py --clobber-config --output output'
   alias src='python read_src_fits.py && head src_fits.csv'
EOF
fi
}
