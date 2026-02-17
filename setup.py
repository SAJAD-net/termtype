from setuptools import setup, find_packages

setup(
    name="termtype",
    version="1.0.0",
    description="A terminal-based typing speed test with multiple template categories",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/termtype",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "windows-curses; platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "termtype=termtype.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.8",
)