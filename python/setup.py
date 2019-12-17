import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mitoscripts",  # Replace with your own username
    version="1.1.0",
    author="Grant Hussey",
    author_email="grant.hussey@nyulangone.org",
    description="To assist in quantifying mitochondrial morphology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/granthussey/MitoScripts",
    packages=['mitoscripts'],#setuptools.find_packages(),
    install_requires=['numpy', 'pandas', 'scikit-learn',
                      'python-igraph', 'matplotlib', 'seaborn'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"mitoscripts": "src/mitoscripts"},
    python_requires=">=3.6",
)
