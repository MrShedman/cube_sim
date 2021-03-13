
from setuptools import setup, find_packages

setup(name="cube_sim",
      version="0.0.1",
      description="RGB cube simulator to aid development.",
      author='Ross Cunningham',
      author_email="MrShedMan",
      url="https://github.com/MrShedman/cube_sim",
      packages=find_packages(),
      install_requires=["pygame", "numpy", "PyGLM", "PyOpenGL", "sphinx"])