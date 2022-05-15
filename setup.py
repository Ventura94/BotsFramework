"""
Setup
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BotsFramework",
    version="0.1.0",
    author="Arian Ventura Rodríguez",
    author_email="arianventura94@gmail.com",
    description="Bots Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ventura94/BotFramework",
    project_urls={
        "Bug Tracker": "https://github.com/ventura94/BotFramework/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["MetaTrader5;platform_system=='Windows'"],
)
