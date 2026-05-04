from setuptools import setup, find_packages

setup(
    name='crypto-market-analyzer',
    version='1.0.0',
    description='Technical analysis tool for altcoins with entry/SL/TP recommendations',
    author='iccky',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'numpy>=1.24.0',
        'click>=8.1.0',
        'colorama>=0.4.6',
    ],
    entry_points={
        'console_scripts': [
            'crypto-analyzer=crypto_analyzer.main:cli',
        ],
    },
    python_requires='>=3.8',
)
