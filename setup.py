# -*- coding: utf-8 -*-
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='botterlord',
      version='0.1',
      description='Retro styled strategy rpg.',
      long_description=readme(),
      url='http://github.com/Marchearth/',
      author='Buğra Coşkun',
      author_email='bgra.coskn@gmail.com',
      license='Apache 2.0',
      packages=['botterlord'],
      install_requires=[
          'PyYaml',
          'screeninfo',
          'pathlib'
      ],
      zip_safe=False,
      test_suite='pytest', test)
