import os


def extract_files(path: str, extension: str):
    """
    Return a list of absolute path of all files of a given
    extension from given path.
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if os.path.splitext(file)[1][1:] == extension:
                files.append(os.path.join(dirpath, file))
    return files
