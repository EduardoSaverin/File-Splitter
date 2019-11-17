import os


def _raise_if_not_exists(filename):
    if not os.path.exists(filename):
        raise Exception(f'File {filename} does not exists.')

def _raise_if_not_directory(filename):
    if not os.path.isfile(filename):
        raise Exception(f"{filename} is not a file")
    
def _raise_if_not_readable(filename):
    if not os.access(filename, os.R_OK):
        raise Exception(f"File {filename} is not readable")

