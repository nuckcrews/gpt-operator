import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gptop",
    version="0.0.1",
    author="Nick Crews",
    description="Handles communication with GPTs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages('src/gptop'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'':'src/gptop'},
    python_requires='>=3.6',
    install_requires=[
        "openai",
        "pinecone-client",
    ]
)
