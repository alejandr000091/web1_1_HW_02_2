#work bot8 version 0.11.8
from setuptools import setup, find_namespace_packages

setup(name = "bot8",
      version="0.11.8",
      license='MIT',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['bot8 = hw_2.bot:main']})