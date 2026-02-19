from setuptools import setup, find_packages

setup(
    name="adorlipi",
    version="0.1.0",
    description="A robust Banglish to Bangla transliteration engine",
    author="AdorLipi Team",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'adorlipi': ['data/*.json', 'assets/*.svg', 'assets/*.png'],
    },
    install_requires=[],
    entry_points={
        'console_scripts': [
            'adorlipi=adorlipi.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
