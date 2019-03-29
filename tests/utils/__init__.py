import os
import shutil


def rm_rf(path):
    assert path != "/"
    if os.path.exists(path):
        shutil.rmtree(path)
