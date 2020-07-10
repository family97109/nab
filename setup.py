from setuptools import setup

setup(
    name='nab',
    version='0.1',
    py_modules=['nab'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        nab=nab:cli
    ''',
)