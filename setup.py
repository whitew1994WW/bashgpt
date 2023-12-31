from setuptools import setup, find_packages

setup(
    name='bashgpt',
    version='0.3.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'bashgpt=bashgpt.bashgpt:main',
        ],
    },
    install_requires=[
    ],
    python_requires='>=3.6',
    description='A cli tool for turning plain text into bash commands',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/whitew1994WW/bashgpt',
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)