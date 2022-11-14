from setuptools import setup, find_packages

version = '2.4'


setup(name='kmd',
      version=version,
      description='An interpreter framework',
      long_description=open('README.rst').read() + '\n' +
                       open('CHANGES.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      keywords='command line, command shell, shell, interpreter, REPL',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/kmd',
      license='PSF-2.0',
      packages=find_packages(
          exclude=[
              'kmd.tests',
          ],
      ),
      include_package_data=False,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'rl >= 3.1',
      ],
      project_urls={
          'Documentation': 'https://kmd.readthedocs.io/en/stable/',
      },
      extras_require={
          'docs': [
              'sphinx == 5.3.0',
              'sphinx-rtd-theme == 1.0.0',
          ],
      },
)
