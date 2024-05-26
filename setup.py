from setuptools import setup, find_packages

setup(
    name='eather-Data-Optimizer',
    version='1.0.0',
    author='Your Name',
    author_email='your@email.com',
    description='A tool for optimizing CSV data and fetching weather information.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'requests',
        'beautifulsoup4',
    ],
)
