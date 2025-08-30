from setuptools import setup
import os

# Get the directory of this file
this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='EasyPygame',
      version='0.1.1',
      description='A plugin to make Pygame easy!',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/RyanKeys/EasyPygame',
      author='Ryan Keys',
      author_email='r.keys1998@gmail.com',
      license='MIT',
      packages=['EasyPygame'],
      install_requires=['pygame'],
      zip_safe=True)
