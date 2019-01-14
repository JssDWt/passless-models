from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='passless_models',
    version='0.0.1',
    install_requires=['jsonpickle', 'python-dateutil'],
    description='Models for Passless infrastructure.',
    long_description=readme(),
    author='Jesse de Wit',
    author_email='witdejesse@hotmail.com',
    license='GPLv3',
    packages= ['passless_models']
)