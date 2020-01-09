import logging
import os
import ntpath
from utils import utils

class SplitFile(object):
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

    def split(self):
        self.logger.info(f"File size : {os.path.getsize(self.file)}")
        self.each_split_size = os.path.getsize(self.file)//self.splits
        self.logger.info(f"Each split size : {self.each_split_size}")
        _, file = ntpath.split(self.file)
        filename, ext = os.path.splitext(file)
        filecount = 1
        self.remaining_splits = self.splits
        with open(self.file, mode="rb",buffering=self.buffer) as in_file:
            while self.remaining_splits > 0:
                output_file = os.path.join(self.outdir,f"{filename}_{filecount}{ext}")
                # Remove if file already exists
                if os.path.exists(output_file) and self.remove_existing:
                    self.logger.debug(f"Removing existing file {output_file}")
                    os.remove(output_file)
                with open(file = output_file, mode="wb",buffering=self.buffer) as out_file:
                    self.logger.info(f'Processing Part {filecount} of {self.file}')
                    self.process_file(in_file,out_file)
                filecount += 1
                self.remaining_splits -= 1
    
    def process_file(self, in_file, output_file):    
        try:
            # If you understand this line then you know how file read/write works
            split_size = os.path.getsize(self.file) if self.remaining_splits == 1 else self.each_split_size
            self.logger.error(f"Split Size : {split_size}")
            chunk_data = in_file.read(split_size)
            print(len(chunk_data))
            if chunk_data != "":
                output_file.write(chunk_data)
        except NameError as e:
            print('Error',e)
            pass

if __name__ == '__main__':
    sp = SplitFile(file='/home/sumit/Python Projects/Python File Splitter & Joiner/test/Spy.mkv',remove_existing=True)
    sp.split()

# Run Command
# python -m splitter.split