from lsst.obs.file.ingest import FileParseTask
config.parse.retarget(FileParseTask)
config.parse.translators = {'fileroot': 'translate_fileroot',
                            'filename': 'translate_filename',
                            'filter':'translate_filter',
                            'extension':'translate_extension'}

#config.register.columns = {'filename': 'text', 'fileroot': 'text', 'filter': 'text', 'extension':'int'}
config.register.columns = {'filename': 'text', 'fileroot': 'text', 'filter': 'text'}

config.register.visit = ['fileroot']
config.register.unique = ['fileroot']
#config.register.unique = ['fileroot', 'extension']