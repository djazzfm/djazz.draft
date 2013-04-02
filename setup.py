#! /usr/bin/env python

from distutils.core import setup
import os

rootpackage = 'djazz'
shareds = ['static', 'templates']

packages = []
for dirpath, dirnames, filenames in os.walk(rootpackage):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        package = '.'.join(dirpath.split('/'))
        packages.append(package)

datas = {}
for package in packages:
    datas[package] = []
    pdir = '/'.join(package.split('.'))
    for shared in shareds:
        sharedpath = '/'.join([pdir, shared])
        if os.path.exists(sharedpath):
            for root, dirs, files in os.walk(sharedpath):
                for f in files:
                    path = '/'.join([root, f])[len(pdir+'/'):]
                    datas[package].append(path)


setup(name='Djazz',
      version='0.1',
      description='Django extension',
      author='Guillaume Dugas',
      author_email='dugas.guillaume@gmail.com',
      url='http://github.com/djazzproject/djazz',
      packages=packages,
      package_data=datas,
      classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: Linux"
        ]
     )
