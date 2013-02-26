#! /usr/bin/env python

from distutils.core import setup
import os


packages = []

for dirpath, dirnames, filenames in os.walk('djazz'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        package = '.'.join(dirpath.split('/'))
        packages.append(package)


datas = {'djazz':       ['templates/djazz/*.html'],
         'djazz.posts': ['templates/djazz/posts/formatters/*.html']}


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
        ],
     )