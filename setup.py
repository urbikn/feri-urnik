import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feri-urnik",
    version="1.0.0",
    author="Urban Knupleš",
    author_email="urbikn@gmail.com",
    description="A FERI schedule running in CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urbikn/feri-urnik",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business :: Scheduling",
        "Operating System :: POSIX :: Linux",
    ],
    keywords='FERI, urnik, scheduler, Wise timetable, timetable, iCal, CLI',
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=['selenium', 'icalevents==0.1.25 ', 'pyyaml', 'fuzzywuzzy', 'Unidecode==1.1.1', "python-Levenshtein"],
    package_data={
        'urnik': ["*.yaml", 'data/*.tar.gz'],
    },
    entry_points={
        'console_scripts': [
            'urnik= urnik.main:main',
        ],
    },
)