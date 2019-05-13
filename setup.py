import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="genealogy",
    version="0.0.2",
    author="Robert Williams",
    author_email="robertedwardwilliams@me.com",
    description="A package for recording Genealogy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kibaffo33/genealogy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
