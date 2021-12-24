import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="num_to_str_repr",
    version="0.0.4",
    author="Iryna Lokhvytska",
    author_email="ilokh@softserveinc.com",
    description="""
    Simple package that converts numbers (int and float)
    to the Russian and Ukrainian string representation.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IrinaLokhvytska/num_to_str_repr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
