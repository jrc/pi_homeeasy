import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pi-homeeasy",
    version="0.0.5",
    author="John Chang",
    author_email="jrcplus+pypi@gmail.com",
    description="Control 433 MHz RF self-learning power outlets (HomeEasy, Nexa, etc.) from a Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrc/pi_homeeasy",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["pi-homeeasy=pi_homeeasy.command_line:main"],},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Home Automation",
    ],
    keywords="433 mHz, rf, homeeasy, home easy, bye bye standby, domia lite, chacon, düwi, byron, intertechno, klikaanklikuit, anslut, proove, nexa, telldus",
    install_requires=["RPi.GPIO"],
    python_requires=">=3.6",
)
