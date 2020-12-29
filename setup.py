import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hevapy",  # Replace with your own username
    version="0.0.2",
    author="Mohit Anand",
    author_email="itsmohitanand@gmail.com",
    description="Hydrological Extreme Value Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/melioristic/hevapy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
