import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mitoscripts_granthussey",  # Replace with your own username
    version="0.5.0",
    author="Grant Hussey",
    author_email="grant.hussey@nyulangone.org",
    description="To assist in quantifying mitochondrial morphology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"mitoscripts": "src/mitoscripts"},
    python_requires=">=3.6",
)
