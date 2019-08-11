from setuptools import find_packages, setup

setup(name='pyykov',
    version='1.1',
    description='Markov generator for python.',
    url='https://github.com/maymike321/pyykov',
    author='Michael May',
    author_email='yamekim@comcast.net',
    packages=find_packages(exclude=("test")),
    license='MIT',
    test_suite='pyykov.pyykov-test.py',
    zip_safe=False)