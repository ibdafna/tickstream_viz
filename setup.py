from setuptools import setup

setup(name='tickstream_viz',
      version='0.1',
      description='Local tick streaming visualisation solution for Jupyter Notebooks',
      url='https://github.com/ibdafna/tickstream_viz',
      author='Itay Dafna',
      author_email='i.b.dafna@gmail.com',
      license='MIT',
      packages=['tickstream_viz'],
      install_requires=['jupyter', 'bqplot', 'numpy', 'pandas', 'ipywidgets', 'zmq'],
      zip_safe=False)