from distutils.core import setup
import os

_this_dir = os.path.dirname(__file__)
README_path = os.path.join(_this_dir, 'README.md')
README = open(README_path).read()


setup(
    name='go_data',
    description='Quick-and-dirty tools for working with Gene Ontology (GO) data.'
    long_description=README,
    version='1.0.0',
    author='Alex Buchanan',
    author_email='buchanae@gmail.com',
    license='MIT',
    py_modules=[
        'go_data',
        'go_data.goa',
    ]
)
