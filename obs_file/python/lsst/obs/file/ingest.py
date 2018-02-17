import os

import lsst.afw.image as afwImage
from lsst.pipe.tasks.ingest import ParseTask

__all__ = ['FileParseTask']


class FileParseTask(ParseTask):
    def getInfo(self, filename):
        """Get information about the image from the filename and its contents

        Here, we open the image and parse the header, but one could also look at the filename itself
        and derive information from that, or set values from the configuration.

        @param filename    Name of file to inspect
        @return File properties; list of file properties for each extension
        """
        md = afwImage.readMetadata(filename, self.config.hdu)
        # We want to use the filename as a key, so putting it in here
        md.set('filename', filename)
        phuInfo = self.getInfoFromMetadata(md)
        if len(self.config.extnames) == 0:
            # No extensions to worry about
            return phuInfo, [phuInfo]
        # Look in the provided extensions
        extnames = set(self.config.extnames)
        extnum = 1
        infoList = []
        while len(extnames) > 0:
            extnum += 1
            try:
                md = afwImage.readMetadata(filename, extnum)
            except:
                self.log.warn("Error reading %s extensions %s" % (filename, extnames))
                break
            ext = self.getExtensionName(md)
            if ext in extnames:
                infoList.append(self.getInfoFromMetadata(md, info=phuInfo.copy()))
                extnames.discard(ext)
        return phuInfo, infoList

    def translate_fileroot(self, md):
        filename = md.get('filename')
        head, tail = os.path.split(filename)
        return tail.split('.')[0]

    def translate_extension(self, md):
        return

    def translate_filter(self, md):
        return 'tmp'

    def translate_filename(self, md):
        head, tail = os.path.split(md.get('filename'))
        return tail

    def getDestination(self, butler, info, filename):
        """Get destination for the file

        @param butler      Data butler
        @param info        File properties, used as dataId for the butler
        @param filename    Input filename
        @return Destination filename
        """
        return butler.get("raw_filename", {'filename': os.path.split(filename)[-1]})[0]
