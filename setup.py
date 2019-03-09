from setuptools import setup, find_packages

version = '2.3'


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
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      keywords='command line shell',
      author='Stefan H. Holek',
      author_email='stefan@epy.co.at',
      url='https://github.com/stefanholek/kmd',
      license='PSFL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='kmd.tests',
      install_requires=[
          'setuptools',
          'rl >= 2.4',
      ],
)
