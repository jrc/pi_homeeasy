import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pi_homeeasy",
    version="0.0.2",
    author="John Chang",
    author_email="jrcplus+pypi@gmail.com",
    description="Control 433 MHz RF self-learning power outlets (HomeEasy/Nexa/etc.) from a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrc/pi_homeeasy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Home Automation",
    ],
    python_requires=">=3.6",
)
