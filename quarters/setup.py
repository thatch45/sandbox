#!/usr/bin/python

from distutils.core import setup

setup(name='quarters',
      version='0.1',
      description='Continuous build system for ArchLinux',
      author='Thomas S Hatch',
      author_email='thatch45@gmail.com',
      url='http://code.google.com/p/enterprise-archlinux/',
      packages=['quarters'],
      scripts=['scripts/quarters'],
      data_files=[('/etc/quarters',
                    ['conf/quarters.conf',
                     'conf/aur-pkgs'
                     ]),
                 ],
     )

