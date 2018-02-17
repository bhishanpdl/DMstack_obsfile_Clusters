from lsst.obs.file.fileisr import FileIsrTask


config.isr.retarget(FileIsrTask)
config.calibrate.doAstrometry = False
config.calibrate.doPhotoCal = False
