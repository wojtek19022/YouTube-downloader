from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("YouTube_video_downloader.py")
)