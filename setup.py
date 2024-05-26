from setuptools import setup, find_packages

setup(
    name='eather-Data-Optimizer',
    version='1.0.0',
    author='shut0',
    author_email='shut0@email.com',
    license=LICENSE,
    description='A tool for optimizing CSV data and fetching weather information.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'beautifulsoup4',
    ],
)
