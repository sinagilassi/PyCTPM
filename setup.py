from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'Python Chemical Thermodynamics for Process Modeling (PyCTPM)'
LONG_DESCRIPTION = 'Python Chemical Thermodynamics for Process Modeling (PyCTPM) is an open-source package which can be used to estimate thermodynamic properties in a typical process modeling'

# Setting up
setup(
    name="PyCTPM",
    version=VERSION,
    author="Sina Gilassi",
    author_email="<sina.gilassi@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    license='MIT',
    install_requires=['numpy',
                      'scipy', 'matplotlib', 'pandas'],
    keywords=['python', 'chemical engineering', 'thermodynamics',
              'process modeling', 'process simulation'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
