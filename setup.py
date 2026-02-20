from setuptools import setup, find_packages

setup(
    name='adorlipi',
    version='1.0.0',
    packages=find_packages(),
    description='AdorLipi - Banglish to Bangla Transliteration Engine',
    author='AdorLipi Team',
    author_email='',
    url='https://github.com/iammhador/adorlipi',
    python_requires='>=3.6',
    license='MIT',
    entry_points={
        'console_scripts': [
            'adorlipi=cli.main:main',
        ],
    },
    package_data={
        '': ['data/*.json', 'assets/*.svg'],
    },
)
