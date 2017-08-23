from setuptools import setup
from glob import glob


setup(
    name='child-support-tables-extractor',
    version='0.2',
    install_requires=[
        'lxml',
    ],
    author='Alex Pilon',
    author_email='alex@miralaw.ca',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    setup_requires=[
        # run pytest, coverage and checks when running python setup.py test.
        'pytest-runner',
        'pytest-cov',
        'pytest-flakes',
    ],
    tests_require=[
        'pytest',
        'coverage',
    ],
    scripts=glob('bin/*'),
)
