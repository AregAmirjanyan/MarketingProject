import pathlib 
from setuptools import setup, find_packages 
 
with open("requirements.txt") as f: 
    reqs = f.read().splitlines() 


with open("docs_requirements.txt") as f: 
    docreqs = f.read().splitlines() 


setup( 
    name="PayOpt", 
    version='1.0.0',
    description="Optimizing the payment process of e-commerce", 
    long_description=pathlib.Path("README.md").read_text(), 
    long_description_content_type="text/markdown", 
    author="Nane Mambreyan, Areg Amirjanyan, Gayane Ohanjanyan, Hasmik Sahakyan", 
    license="MIT", 
    classifiers=[ 
        "Development Status :: 3 - Alpha" 
    ], 
    python_requires=">=3.8.2, <3.12",  
    install_requires=[reqs, docreqs], 
    packages=find_packages(include=["Documents", "payment_optimizer", 'payment_optimizer.*', 'test', 'tests.*']), 
    package_data={
        '': ['DB.md', 'api.md', 'Model.md', 'logger.md'],  # Include specific documentation files
    }
)
