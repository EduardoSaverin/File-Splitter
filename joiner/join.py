import logging
import os
import ntpath
from utils import utils

class JoinFile(object):
    def __init__(self, file, out_dir = '.', num_of_splits=3,remove_existing=False,buffer=1024*1024*1024*1):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing File Split")
        
        utils._raise_if_not_exists(file)
        utils._raise_if_not_directory(file)
        utils._raise_if_not_readable(file)

        self.file = file
        self.splits = num_of_splits
        self.outdir = out_dir
        self.buffer = buffer # 1GB Default, Reduce this buffer if your device is a small enough like rasp
        self.remove_existing = remove_existing
        self.logger.info("Initialization Done")

    def join(self):
        _, file = ntpath.split(self.file)
        filename,ext = os.path.splitext(file)
        out_file = open(file,mode="wb",buffering=self.buffer)
        for i in range(0,self.splits):
            with open(filename+"_"+str(i+1)+ext,mode="rb") as in_file:
                out_file.write(in_file.read())
        out_file.close()

if __name__ == '__main__':
    sp = JoinFile(file='/home/sumit/Python Projects/Python File Splitter & Joiner/test/Spy.mkv',remove_existing=True)
    sp.join()

# Run Command
# python -m splitter.split