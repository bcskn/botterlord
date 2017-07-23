from setuptools import setup

setup(name='botterlord',
      version='0.1',
      description='Retro styled strategy rpg.',
      url='http://github.com/Marchearth/',
      author='Buğra Coşkun',
      author_email='mentalnerd1@gmail.com',
      license='Apache 2.0',
      packages=['botterlord'],
      install_requires=[
          'PyYaml',
          'screeninfo'
      ],
      zip_safe=False)
