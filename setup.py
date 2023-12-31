from setuptools import setup, find_packages

setup(
    name='your_package',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bashgpt=bash_runner:main',
        ],
    },
    install_requires=[
    ],
    python_requires='>=3.6',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your project.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package',
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)