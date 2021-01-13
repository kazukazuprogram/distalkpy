from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="distalkpy",
    version="0.0.0",
    license="MIT",
    author="kazukazuprogram",
    packages=["src"],
    description="Read aloud the message that came to Discord on the voice channel",
    long_description=long_description,
    install_requires=open("requirements.txt").read().strip().splitlines(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Natural Language :: English",
        "Topic :: Utilities",
        # 'License :: OSI Approved :: Python Software Foundation License',
        # 'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        # 'Operating System :: POSIX'
    ],
    entry_points={
        "console_scripts": [
            "distalkpy = distalkpy.__main__:main",
        ]
    }
)
