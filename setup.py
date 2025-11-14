# setup.py  
from setuptools import setup, find_packages  
 
setup(  
    name="emc_tools",
    version="0.1.0",  
    packages=find_packages(where="src"),  # Finds packages under src/  
    package_dir={"": "src"},  # Tells setuptools packages are in src/  
    install_requires=[],  # Add dependencies here
)  