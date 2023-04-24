import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gptop",
    version="0.0.6",
    author="Nick Crews",
    description="Handles communication with GPTs",
    keywords="gptop GPT operator llm ai",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=[
        "tests",
        "scripts",
        "example",
        "cli"
    ]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "requests >= 2.20",
        "scikit-learn >= 1.0.2",
        "tenacity >= 8.0.1",
        "matplotlib",
        "plotly",
        "numpy",
        "scipy",
        "pandas >= 1.2.3",
        "pandas-stubs >= 1.1.0.11",
        "openpyxl >= 3.0.7",
        "aiohttp",
        "tqdm",
        "pyyaml >= 5.4",
        "loguru >= 0.5.0",
        "typing-extensions >= 3.7.4",
        "dnspython >= 2.0.0",
        "python_dateutil >= 2.5.3",
        "urllib3 >= 1.21.1",
        "openai",
        "pinecone-client",
    ]
)
