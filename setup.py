import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feri-urnik",
    version="0.0.2",
    author="Urban Knupleš",
    author_email="urbikn@gmail.com",
    description="A FERI schedule application running in CLI ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/urbikn/feri-urnik",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Office/Business :: Scheduling",
        "Development Status :: 4 - Beta",
        "Operating System :: POSIX :: Linux",
    ],
    keywords='FERI, urnik, scheduler, wisetimetable, iCal',
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=['selenium', 'icalevents', 'pyyaml', 'fuzzywuzzy', 'unidecode'],
    package_data={
        'geckodriver': ['geckodriver-v0.28.0-linux64.tar.gz'],
        'config': ['config.yaml'],
    },

)