import os
from setuptools import setup, find_packages

from dockerfile_bakery.about import __version__, __description__


def requirements():
    reqfile = 'requirements.txt'
    with open(os.path.join(os.path.dirname(__file__), reqfile)) as f:
        return f.read().splitlines()


setup(name='dockerfile_bakery',
      version=__version__,
      description=__description__,
      author='kujyp',
      author_email='pjo901018@gmail.com',
      url='https://github.com/kujyp/dockerfile_bakery',
      packages=find_packages(exclude=[]),
      entry_points='''
        [console_scripts]
        dockerfile_bakery = dockerfile_bakery.cli:main
      ''',
      include_package_data=True,
      install_requires=requirements())
