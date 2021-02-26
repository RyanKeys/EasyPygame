from setuptools import setup


with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='EasyPygame',
      version='0.1.1',
      description='A plugin to make Pygame easy!',
      long_description=long_description,
      url='https://github.com/RyanKeys/EzPygame',
      author='Ryan Keys',
      author_email='r.keys1998@gmail.com',
      license='MIT',
      packages=['EasyPygame'],
      zip_safe=True)


install_requires=['pygame']