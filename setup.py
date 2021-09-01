from setuptools import setup, find_packages

setup(
    name='pynetfuzz',
    version='1.0.0',
    description='Create network fuzz with a simple python package',
    author='James Wingar',
    url='https://github.com/JamesWingar/PyNetFuzz',
    packages=find_packages(include=['pynetfuzz', 'pynetfuzz.*']),
    install_requires=[
        'psutil==5.8.0',
        'scapy==2.4.5'
    ],
)