from setuptools import setup

setup(name='pyqhtools',
      version='0.1',
      description='Queensland Hydrology Tools',
      url='http://github.com/chasegan/pyqhtools',
      author='Chas Egan',
      author_email='thecosmologist@gmail.com',
      license='MIT',
      packages=['pyqhtools'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
